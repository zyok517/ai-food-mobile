import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import json
import secrets
from sqlalchemy import create_engine, text
from .ai_service import analyze

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

DB_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST', '127.0.0.1')}:{os.getenv('DB_PORT', '3306')}"
    f"/{os.getenv('DB_NAME', 'ai_food')}?charset=utf8mb4"
)
engine = create_engine(DB_URL, pool_pre_ping=True)


@asynccontextmanager
async def lifespan(_: FastAPI):
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        has_meal_id = connection.execute(text("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='ratings' AND COLUMN_NAME='meal_id'
        """)).scalar()
        if not has_meal_id:
            connection.commit()
            connection.execute(text("ALTER TABLE ratings ADD COLUMN meal_id BIGINT NULL AFTER dish_id"))
            connection.commit()
    yield
    engine.dispose()


app = FastAPI(title="AI 助食 API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUTH_TOKENS: dict[str, int] = {}


class AIRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1200)
    goal: str = Field(default="维持", pattern="^(维持|减脂|增肌)$")
    allergies: str = Field(default="", max_length=200)
    dislikes: list[str] = Field(default_factory=list, max_length=20)


@app.post("/api/ai/analyze")
def ai_analyze(payload: AIRequest):
    if not payload.message.strip():
        raise HTTPException(422, "请输入菜品或饮食问题")
    if not os.getenv("DEEPSEEK_API_KEY", "").strip():
        raise HTTPException(503, "请在项目 .env 中填写 DEEPSEEK_API_KEY 并重启后端")
    with engine.connect() as connection:
        rows = [dict(row) for row in connection.execute(text("SELECT id, name, kcal, protein, fat, carbs FROM dishes")).mappings()]
    with open(os.path.join(os.path.dirname(__file__), "nutrition_knowledge.json"), encoding="utf-8") as file:
        knowledge = json.load(file)
    return analyze(payload.message, {"goal": payload.goal, "allergies": payload.allergies, "dislikes": payload.dislikes}, rows, knowledge)


class RatingCreate(BaseModel):
    user_id: int = Field(gt=0)
    meal_id: int = Field(gt=0)
    overall_score: int = Field(ge=1, le=5)
    taste_score: int | None = Field(default=None, ge=1, le=5)
    value_score: int | None = Field(default=None, ge=1, le=5)
    comment: str | None = Field(default=None, max_length=200)
    quick_tags: list[str] = Field(default_factory=list)


class MealCreate(BaseModel):
    user_id: int = Field(gt=0)
    dish_id: int = Field(gt=0)
    source: str = Field(default="catalog", pattern="^(swipe|roulette|catalog|home)$")


def _rating_summary(connection, dish_id: int):
    row = connection.execute(text("""
        SELECT COUNT(*) AS rating_count, COALESCE(AVG(overall_score), 0) AS rating_avg,
               COALESCE(AVG(taste_score), 0) AS taste_avg, COALESCE(AVG(value_score), 0) AS value_avg
        FROM ratings WHERE dish_id=:dish_id
    """), {"dish_id": dish_id}).mappings().one()
    total = connection.execute(text("SELECT COALESCE(AVG(overall_score), 0) FROM ratings")).scalar() or 0
    v = int(row["rating_count"] or 0)
    r = float(row["rating_avg"] or 0)
    m = 10
    weighted = ((v / (v + m)) * r + (m / (v + m)) * float(total)) if v else 0
    return {"rating_count": v, "rating_avg": round(r, 2), "taste_avg": round(float(row["taste_avg"] or 0), 2), "value_avg": round(float(row["value_avg"] or 0), 2), "weighted_score": round(weighted, 3)}


class UserCreate(BaseModel):
    phone: str = Field(min_length=3, max_length=20)
    nickname: str = Field(default="校园吃货", min_length=1, max_length=50)


class SendCodeRequest(BaseModel):
    phone: str = Field(min_length=6, max_length=20)


class LoginRequest(BaseModel):
    phone: str = Field(min_length=6, max_length=20)
    code: str = Field(min_length=4, max_length=8)
    nickname: str = Field(default="校园吃货", min_length=1, max_length=50)


class PreferenceUpdate(BaseModel):
    taste_tags: list[str] = Field(default_factory=list)
    dislike_tags: list[str] = Field(default_factory=list)
    allergies: list[str] = Field(default_factory=list)
    goal: str = Field(default="维持", pattern="^(维持|减脂|增肌)$")


@app.get("/api/health")
def health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}


@app.post("/api/auth/send-code")
def send_login_code(payload: SendCodeRequest):
    return {"status": "sent", "demo_code": "123456", "message": "开发环境验证码为 123456"}


@app.post("/api/auth/login")
def login(payload: LoginRequest):
    if payload.code != "123456":
        raise HTTPException(status_code=401, detail="验证码错误或已过期")
    with engine.begin() as connection:
        user = connection.execute(text("SELECT id, phone, nickname FROM users WHERE phone=:phone"), {"phone": payload.phone}).mappings().first()
        if user is None:
            result = connection.execute(text("INSERT INTO users (phone, nickname) VALUES (:phone, :nickname)"), payload.model_dump(exclude={"code"}))
            user = {"id": result.lastrowid, "phone": payload.phone, "nickname": payload.nickname}
        else:
            user = dict(user)
    token = secrets.token_urlsafe(32)
    AUTH_TOKENS[token] = int(user["id"])
    return {"token": token, "user": user}


@app.get("/api/auth/me")
def current_user(authorization: str | None = Header(default=None)):
    token = (authorization or "").removeprefix("Bearer ").strip()
    user_id = AUTH_TOKENS.get(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="登录已失效")
    with engine.connect() as connection:
        user = connection.execute(text("SELECT id, phone, nickname FROM users WHERE id=:id"), {"id": user_id}).mappings().first()
    if user is None:
        raise HTTPException(status_code=401, detail="用户不存在")
    return dict(user)


@app.post("/api/users", status_code=201)
def create_user(payload: UserCreate):
    with engine.begin() as connection:
        existing = connection.execute(text("SELECT id, phone, nickname FROM users WHERE phone=:phone"), {"phone": payload.phone}).mappings().first()
        if existing:
            return dict(existing)
        result = connection.execute(text("INSERT INTO users (phone, nickname) VALUES (:phone, :nickname)"), payload.model_dump())
        return {"id": result.lastrowid, "phone": payload.phone, "nickname": payload.nickname}


@app.get("/api/users/{user_id}/preferences")
def get_preferences(user_id: int):
    sql = text("SELECT u.id, u.nickname, u.goal, p.taste_tags, p.dislike_tags, p.allergies FROM users u LEFT JOIN user_preferences p ON p.user_id=u.id WHERE u.id=:id")
    with engine.connect() as connection:
        row = connection.execute(sql, {"id": user_id}).mappings().first()
    if row is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    result = dict(row)
    for key in ("taste_tags", "dislike_tags", "allergies"):
        result[key] = json.loads(result[key]) if isinstance(result[key], str) else (result[key] or [])
    return result


@app.put("/api/users/{user_id}/preferences")
def update_preferences(user_id: int, payload: PreferenceUpdate):
    with engine.begin() as connection:
        if connection.execute(text("SELECT 1 FROM users WHERE id=:id"), {"id": user_id}).first() is None:
            raise HTTPException(status_code=404, detail="用户不存在")
        connection.execute(text("UPDATE users SET goal=:goal WHERE id=:id"), {"goal": payload.goal, "id": user_id})
        connection.execute(text("INSERT INTO user_preferences (user_id, taste_tags, dislike_tags, allergies) VALUES (:user_id,:taste_tags,:dislike_tags,:allergies) ON DUPLICATE KEY UPDATE taste_tags=VALUES(taste_tags), dislike_tags=VALUES(dislike_tags), allergies=VALUES(allergies)"), {
            "user_id": user_id,
            "taste_tags": json.dumps(payload.taste_tags, ensure_ascii=False),
            "dislike_tags": json.dumps(payload.dislike_tags, ensure_ascii=False),
            "allergies": json.dumps(payload.allergies, ensure_ascii=False),
        })
    return {"status": "updated"}


@app.get("/api/cafeterias")
def list_cafeterias():
    sql = text("SELECT id, name FROM cafeterias ORDER BY id")
    with engine.connect() as connection:
        return [dict(row) for row in connection.execute(sql).mappings()]


@app.get("/api/cafeterias/{cafeteria_id}/windows")
def list_windows(cafeteria_id: int, floor: int | None = Query(default=None, ge=1)):
    sql = text(
        "SELECT id, cafeteria_id, floor, name "
        "FROM windows WHERE cafeteria_id = :cafeteria_id "
        "AND (:floor IS NULL OR floor = :floor) ORDER BY floor, id"
    )
    params = {"cafeteria_id": cafeteria_id, "floor": floor}
    with engine.connect() as connection:
        return [dict(row) for row in connection.execute(sql, params).mappings()]


@app.get("/api/windows/{window_id}/dishes")
def list_window_dishes(window_id: int):
    sql = text(
        "SELECT id, name, window_id, price, rating, count AS rating_count, "
        "taste, ingredients, kcal, protein, fat, carbs, crop, image_url "
        "FROM dishes WHERE window_id = :window_id ORDER BY id"
    )
    with engine.connect() as connection:
        return [dict(row) for row in connection.execute(sql, {"window_id": window_id}).mappings()]


@app.get("/api/dishes/{dish_id}")
def get_dish(dish_id: int):
    sql = text(
        "SELECT id, name, window_id, price, rating, count AS rating_count, "
        "taste, ingredients, kcal, protein, fat, carbs, crop, image_url "
        "FROM dishes WHERE id = :dish_id"
    )
    with engine.connect() as connection:
        dish = connection.execute(sql, {"dish_id": dish_id}).mappings().first()
    if dish is None:
        raise HTTPException(status_code=404, detail="菜品不存在")
    result = dict(dish)
    with engine.connect() as connection:
        result.update(_rating_summary(connection, dish_id))
    return result


@app.get("/api/dishes")
def search_dishes(q: str = "", limit: int = Query(default=50, ge=1, le=200)):
    sql = text(
        "SELECT d.id, d.name, d.window_id, d.price, d.rating, "
        "d.count AS rating_count, d.taste, d.ingredients, d.kcal, "
        "d.protein, d.fat, d.carbs, d.crop, d.image_url, "
        "w.name AS window_name, c.id AS cafeteria_id, c.name AS cafeteria_name "
        "FROM dishes d JOIN windows w ON w.id = d.window_id "
        "JOIN cafeterias c ON c.id = w.cafeteria_id "
        "WHERE :q = '' OR d.name LIKE :like_q OR w.name LIKE :like_q OR c.name LIKE :like_q "
        "ORDER BY d.id LIMIT :limit"
    )
    params = {"q": q.strip(), "like_q": f"%{q.strip()}%", "limit": limit}
    with engine.connect() as connection:
        return [dict(row) for row in connection.execute(sql, params).mappings()]


@app.get("/api/dishes/{dish_id}/ratings")
def list_ratings(dish_id: int, limit: int = Query(default=50, ge=1, le=100), exclude_user_id: int | None = Query(default=None, ge=1)):
    sql = text(
        "SELECT r.id, r.user_id, u.nickname, r.overall_score, r.taste_score, "
        "r.value_score, r.comment, r.quick_tags, r.created_at "
        "FROM ratings r JOIN users u ON u.id = r.user_id "
        "WHERE r.dish_id = :dish_id AND (:exclude_user_id IS NULL OR r.user_id <> :exclude_user_id) "
        "ORDER BY r.created_at DESC LIMIT :limit"
    )
    with engine.connect() as connection:
        rows = [dict(row) for row in connection.execute(sql, {"dish_id": dish_id, "limit": limit, "exclude_user_id": exclude_user_id}).mappings()]
    for row in rows:
        if isinstance(row.get("quick_tags"), str):
            row["quick_tags"] = json.loads(row["quick_tags"])
    return rows


@app.post("/api/users/{user_id}/meals", status_code=201)
def create_meal(user_id: int, payload: MealCreate):
    if payload.user_id != user_id:
        raise HTTPException(status_code=403, detail="用户身份不匹配")
    with engine.begin() as connection:
        if connection.execute(text("SELECT 1 FROM users WHERE id=:id"), {"id": user_id}).first() is None:
            raise HTTPException(status_code=404, detail="用户不存在")
        if connection.execute(text("SELECT 1 FROM dishes WHERE id=:id"), {"id": payload.dish_id}).first() is None:
            raise HTTPException(status_code=404, detail="菜品不存在")
        existing = connection.execute(text("""
            SELECT id, user_id, dish_id, source, eaten_at, review_status
            FROM meal_records WHERE user_id=:user_id AND dish_id=:dish_id
              AND eaten_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
            ORDER BY eaten_at DESC LIMIT 1
        """), {"user_id": user_id, "dish_id": payload.dish_id}).mappings().first()
        if existing:
            return {**dict(existing), "status": "existing"}
        result = connection.execute(text("""
            INSERT INTO meal_records (user_id, dish_id, source) VALUES (:user_id, :dish_id, :source)
        """), payload.model_dump())
        return {"id": result.lastrowid, "user_id": user_id, "dish_id": payload.dish_id, "review_status": "pending", "status": "created"}


@app.get("/api/users/{user_id}/meals/pending-reviews")
def pending_reviews(user_id: int):
    sql = text("""
        SELECT m.id AS meal_id, m.dish_id, m.eaten_at, d.name, d.price, d.image_url,
               w.name AS window_name, c.name AS cafeteria_name
        FROM meal_records m JOIN dishes d ON d.id=m.dish_id
        JOIN windows w ON w.id=d.window_id JOIN cafeterias c ON c.id=w.cafeteria_id
        WHERE m.user_id=:user_id AND m.review_status='pending'
        ORDER BY m.eaten_at DESC
    """)
    with engine.connect() as connection:
        return [dict(row) for row in connection.execute(sql, {"user_id": user_id}).mappings()]


@app.post("/api/dishes/{dish_id}/ratings", status_code=201)
def create_rating(dish_id: int, payload: RatingCreate):
    with engine.begin() as connection:
        if connection.execute(text("SELECT 1 FROM dishes WHERE id=:id"), {"id": dish_id}).first() is None:
            raise HTTPException(status_code=404, detail="菜品不存在")
        if connection.execute(text("SELECT 1 FROM users WHERE id=:id"), {"id": payload.user_id}).first() is None:
            raise HTTPException(status_code=404, detail="用户不存在")
        meal = connection.execute(text("""
            SELECT id, review_status FROM meal_records
            WHERE id=:meal_id AND user_id=:user_id AND dish_id=:dish_id
        """), {"meal_id": payload.meal_id, "user_id": payload.user_id, "dish_id": dish_id}).mappings().first()
        if meal is None:
            raise HTTPException(status_code=403, detail="请先记录吃过这道菜")
        if meal["review_status"] == "reviewed":
            raise HTTPException(status_code=409, detail="这条用餐记录已经评价过")
        result = connection.execute(text(
            "INSERT INTO ratings (user_id, dish_id, meal_id, overall_score, taste_score, value_score, comment, quick_tags) "
            "VALUES (:user_id, :dish_id, :meal_id, :overall_score, :taste_score, :value_score, :comment, :quick_tags)"
        ), {**payload.model_dump(exclude={"quick_tags"}), "dish_id": dish_id,
            "quick_tags": json.dumps(payload.quick_tags, ensure_ascii=False)})
        connection.execute(text("UPDATE meal_records SET review_status='reviewed' WHERE id=:meal_id"), {"meal_id": payload.meal_id})
        summary = _rating_summary(connection, dish_id)
        connection.execute(text("UPDATE dishes SET rating=:rating, count=:count WHERE id=:dish_id"), {"rating": summary["rating_avg"], "count": summary["rating_count"], "dish_id": dish_id})
        return {"id": result.lastrowid, "status": "created", **summary}


@app.get("/api/rankings")
def rankings(period: str = Query(default="week", pattern="^(week|month)$"), limit: int = Query(default=10, ge=1, le=50)):
    interval = "7 DAY" if period == "week" else "1 MONTH"
    safe_limit = limit if isinstance(limit, int) else 10
    sql = text(f"""
        SELECT d.id, d.name, d.price, d.image_url, w.name AS window_name,
               c.name AS cafeteria_name, COUNT(r.id) AS rating_count,
               AVG(r.overall_score) AS rating_avg,
               COUNT(DISTINCT m.id) AS meal_count
        FROM dishes d JOIN windows w ON w.id=d.window_id JOIN cafeterias c ON c.id=w.cafeteria_id
        LEFT JOIN ratings r ON r.dish_id=d.id AND r.created_at >= DATE_SUB(NOW(), INTERVAL {interval})
        LEFT JOIN meal_records m ON m.dish_id=d.id AND m.eaten_at >= DATE_SUB(NOW(), INTERVAL {interval})
        GROUP BY d.id, d.name, d.price, d.image_url, w.name, c.name
        HAVING COUNT(r.id) > 0
        ORDER BY (AVG(r.overall_score) * COUNT(r.id) / (COUNT(r.id) + 10)) DESC, COUNT(r.id) DESC
        LIMIT {safe_limit}
    """)
    with engine.connect() as connection:
        rows = [dict(row) for row in connection.execute(sql).mappings()]
    for index, row in enumerate(rows, start=1):
        row["rank_no"] = index
        row["rating_avg"] = round(float(row["rating_avg"] or 0), 2)
    return rows
