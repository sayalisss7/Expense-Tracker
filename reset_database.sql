-- ============================================================
--  reset_database.sql
--  Use this if you get column errors or want a clean slate.
--  WARNING: This DELETES all existing data.
--  Run: mysql -u root -p < reset_database.sql
-- ============================================================

DROP DATABASE IF EXISTS expense_tracker;

CREATE DATABASE expense_tracker
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE expense_tracker;

-- ── Categories ────────────────────────────────────────────
CREATE TABLE categories (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL UNIQUE,
    icon       VARCHAR(10)  DEFAULT '💰',
    color      VARCHAR(20)  DEFAULT '#6C63FF',
    created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO categories (name, icon, color) VALUES
  ('Food & Dining',     '🍔', '#FF6B6B'),
  ('Transportation',    '🚗', '#4ECDC4'),
  ('Shopping',          '🛍️', '#45B7D1'),
  ('Entertainment',     '🎬', '#96CEB4'),
  ('Health & Medical',  '🏥', '#FFEAA7'),
  ('Utilities',         '💡', '#DDA0DD'),
  ('Housing',           '🏠', '#98D8C8'),
  ('Education',         '📚', '#F7DC6F'),
  ('Travel',            '✈️', '#85C1E9'),
  ('Personal Care',     '💄', '#F1948A'),
  ('Investments',       '📈', '#82E0AA'),
  ('Other',             '📦', '#BDC3C7');

-- ── Users ─────────────────────────────────────────────────
CREATE TABLE users (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    username       VARCHAR(100)   NOT NULL UNIQUE,
    email          VARCHAR(255)   NOT NULL UNIQUE,
    monthly_budget DECIMAL(12, 2) DEFAULT 0.00,
    created_at     TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email, monthly_budget)
VALUES ('default_user', 'user@expensetracker.com', 50000.00);

-- ── Expenses ──────────────────────────────────────────────
CREATE TABLE expenses (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT            NOT NULL,
    category_id  INT            NOT NULL,
    title        VARCHAR(255)   NOT NULL,
    amount       DECIMAL(12, 2) NOT NULL CHECK (amount > 0),
    expense_date DATE           NOT NULL,
    description  TEXT,
    payment_mode ENUM('Cash','Card','UPI','Net Banking','Other') DEFAULT 'Cash',
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)     REFERENCES users(id)      ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT
);

-- ── Income ────────────────────────────────────────────────
CREATE TABLE income (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT            NOT NULL,
    source      VARCHAR(255)   NOT NULL,
    amount      DECIMAL(12, 2) NOT NULL CHECK (amount > 0),
    income_date DATE           NOT NULL,
    description TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ── Budgets ───────────────────────────────────────────────
CREATE TABLE budgets (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT            NOT NULL,
    category_id INT            NOT NULL,
    month_year  VARCHAR(7)     NOT NULL,
    budget_amt  DECIMAL(12, 2) NOT NULL CHECK (budget_amt >= 0),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_user_cat_month (user_id, category_id, month_year),
    FOREIGN KEY (user_id)     REFERENCES users(id)      ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- ── View ──────────────────────────────────────────────────
CREATE VIEW vw_expense_summary AS
SELECT
    e.id,
    u.username,
    c.name        AS category,
    c.icon        AS category_icon,
    c.color       AS category_color,
    e.title,
    e.amount,
    e.expense_date,
    e.description,
    e.payment_mode,
    e.created_at
FROM expenses e
JOIN users      u ON e.user_id     = u.id
JOIN categories c ON e.category_id = c.id;

SELECT 'Database reset complete! ✅' AS status;
