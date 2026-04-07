-- ============================================================
--  Expense Tracker - MySQL Database Setup
--  Run this file FIRST before launching the app
-- ============================================================

CREATE DATABASE IF NOT EXISTS expense_tracker
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE expense_tracker;

-- ── Categories table ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS categories (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL UNIQUE,
    icon       VARCHAR(10)  DEFAULT '💰',
    color      VARCHAR(20)  DEFAULT '#6C63FF',
    created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- Seed default categories
INSERT IGNORE INTO categories (name, icon, color) VALUES
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

-- ── Users table ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    username     VARCHAR(100) NOT NULL UNIQUE,
    email        VARCHAR(255) NOT NULL UNIQUE,
    monthly_budget DECIMAL(12, 2) DEFAULT 0.00,
    created_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- Default user so the app works immediately
INSERT IGNORE INTO users (username, email, monthly_budget)
VALUES ('default_user', 'user@expensetracker.com', 50000.00);

-- ── Expenses table ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS expenses (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT            NOT NULL,
    category_id  INT            NOT NULL,
    title        VARCHAR(255)   NOT NULL,
    amount       DECIMAL(12, 2) NOT NULL CHECK (amount > 0),
    expense_date DATE           NOT NULL,
    description  TEXT,
    payment_mode ENUM('Cash','Card','UPI','Net Banking','Other') DEFAULT 'Cash',
    created_at   TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP      DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)     REFERENCES users(id)      ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT
);

ALTER TABLE expenses 
MODIFY payment_mode ENUM('Cash','Card','UPI','Net Banking','Wallet','Other');

-- ── Income table ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS income (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT            NOT NULL,
    source      VARCHAR(255)   NOT NULL,
    amount      DECIMAL(12, 2) NOT NULL CHECK (amount > 0),
    income_date DATE           NOT NULL,
    description TEXT,
    created_at  TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ── Budgets table (per-category monthly budget) ───────────
CREATE TABLE IF NOT EXISTS budgets (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT            NOT NULL,
    category_id INT            NOT NULL,
    month_year  VARCHAR(7)     NOT NULL COMMENT 'Format: YYYY-MM',
    budget_amt  DECIMAL(12, 2) NOT NULL CHECK (budget_amt >= 0),
    created_at  TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_user_cat_month (user_id, category_id, month_year),
    FOREIGN KEY (user_id)     REFERENCES users(id)      ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- ── Handy views ───────────────────────────────────────────
CREATE OR REPLACE VIEW vw_expense_summary AS
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

SELECT 'Database setup complete! ✅' AS status;
