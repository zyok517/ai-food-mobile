import unittest
from unittest.mock import patch
from fastapi import HTTPException
from backend.ai_service import analyze, model_json, retrieve


class NutritionTests(unittest.TestCase):
    def test_quantity_database_precedence_and_energy_shares(self):
        parsed = {"intent": "nutrition", "scope": "meal", "foods": [{"name": "番茄炒蛋", "quantity": 2, "portion": "普通一份", "kcal": 999, "protein": 1, "fat": 1, "carbs": 1}]}
        row = {"id": 1, "name": "番茄炒蛋", "kcal": 200, "protein": 10, "fat": 8, "carbs": 22}
        with patch('backend.ai_service.model_json', side_effect=[parsed, {"evaluation": "搭配蔬菜", "suggestions": ["增加蔬菜"]}]):
            result = analyze("两份番茄炒蛋", {}, [row], [])
        self.assertEqual(result['totals']['kcal'], 400)
        self.assertEqual(result['totals']['protein'], 20)
        self.assertEqual(result['foods'][0]['source'], '菜品库预设值')
        self.assertIsNone(result['foods'][0]['fiber'])
        self.assertAlmostEqual(sum(result['shares'].values()), 100, places=0)

    def test_missing_values_use_estimate_not_zero(self):
        parsed = {"intent": "nutrition", "foods": [{"name": "米饭", "quantity": .5, "kcal": 200, "protein": 4, "fat": 1, "carbs": 45}]}
        with patch('backend.ai_service.model_json', side_effect=[parsed, {"evaluation": "估算", "suggestions": []}]):
            result = analyze("半份米饭", {}, [{"id": 1, "name": "米饭", "kcal": None}], [])
        self.assertEqual(result['totals']['kcal'], 100)
        self.assertIn('AI', result['foods'][0]['source'])

    def test_question_does_not_invent_foods(self):
        with patch('backend.ai_service.model_json', side_effect=[{"intent": "question", "foods": []}, {"answer": "少盐少油", "evaluation": "", "suggestions": []}]):
            result = analyze("油腻怎么办", {}, [], [])
        self.assertEqual(result['foods'], [])
        self.assertEqual(result['answer'], '少盐少油')

    def test_missing_key_is_explicit(self):
        with patch.dict('os.environ', {'DEEPSEEK_API_KEY': ''}):
            with self.assertRaises(HTTPException) as error:
                model_json('test', {})
        self.assertEqual(error.exception.status_code, 503)

    def test_retrieval_no_unrelated_match(self):
        self.assertEqual(retrieve('米饭', [{'name': '牛肉'}], lambda x: x['name']), [])


if __name__ == '__main__':
    unittest.main()
