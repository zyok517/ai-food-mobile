-- AI 助食业务扩展表
-- 使用前请先执行 ai_food_import.sql，确保 cafeterias/windows/dishes 已存在。
USE ai_food;

CREATE TABLE IF NOT EXISTS users (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  phone VARCHAR(20) NOT NULL UNIQUE,
  nickname VARCHAR(50) NOT NULL DEFAULT '校园吃货',
  avatar_url VARCHAR(500),
  goal ENUM('维持', '减脂', '增肌') NOT NULL DEFAULT '维持',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_users_phone (phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS user_preferences (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL UNIQUE,
  taste_tags JSON NOT NULL,
  dislike_tags JSON NOT NULL,
  allergies JSON NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_preferences_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ratings (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  dish_id BIGINT NOT NULL,
  meal_id BIGINT,
  overall_score TINYINT NOT NULL,
  taste_score TINYINT,
  value_score TINYINT,
  comment VARCHAR(200),
  quick_tags JSON NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT chk_ratings_overall CHECK (overall_score BETWEEN 1 AND 5),
  CONSTRAINT chk_ratings_taste CHECK (taste_score IS NULL OR taste_score BETWEEN 1 AND 5),
  CONSTRAINT chk_ratings_value CHECK (value_score IS NULL OR value_score BETWEEN 1 AND 5),
  CONSTRAINT fk_ratings_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  CONSTRAINT fk_ratings_dish FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE,
  INDEX idx_ratings_dish_created (dish_id, created_at),
  INDEX idx_ratings_user_created (user_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS meal_records (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  dish_id BIGINT NOT NULL,
  source ENUM('swipe', 'roulette', 'catalog', 'home') NOT NULL DEFAULT 'catalog',
  eaten_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  review_status ENUM('pending', 'reviewed') NOT NULL DEFAULT 'pending',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_meal_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  CONSTRAINT fk_meal_dish FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE,
  UNIQUE KEY uk_meal_user_dish_time (user_id, dish_id, eaten_at),
  INDEX idx_meal_pending (user_id, review_status, eaten_at),
  INDEX idx_meal_dish (dish_id, eaten_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS rank_snapshots (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  period_type ENUM('week', 'month') NOT NULL,
  period_start DATE NOT NULL,
  period_end DATE NOT NULL,
  rank_no TINYINT NOT NULL,
  dish_id BIGINT NOT NULL,
  weighted_score DECIMAL(4,2) NOT NULL,
  rating_count INT NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_rank_dish FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE,
  UNIQUE KEY uk_rank_period (period_type, period_start, rank_no),
  INDEX idx_rank_lookup (period_type, period_start)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ai_conversations (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT,
  user_message TEXT NOT NULL,
  assistant_message TEXT NOT NULL,
  matched_dishes JSON,
  nutrition_summary JSON,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_ai_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
  INDEX idx_ai_user_created (user_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
