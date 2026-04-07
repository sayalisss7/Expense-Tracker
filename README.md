# 💸 SpendWise — MySQL Expense Tracker

A full-featured personal expense tracker built with **Python**, **Streamlit**, and **MySQL**.

---

## 📁 Project Structure

```
expense_tracker/
├── setup_database.sql   ← Step 1: Run this in MySQL first
├── config.py            ← Step 2: Update your DB credentials here
├── db_operations.py     ← CRUD layer (no need to edit)
├── app.py               ← Step 3: Run this with Streamlit
├── requirements.txt     ← Python dependencies
└── README.md
```

---

## 🚀 Setup & Run (in order)

### Step 1 — Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 2 — Set up the MySQL database

Open your MySQL client (MySQL Workbench, terminal, etc.) and run:

```sql
source setup_database.sql;
-- or paste the file contents directly
```

This creates the `expense_tracker` database, all tables, and seeds 12 default categories.

### Step 3 — Configure your DB credentials

Open `config.py` and update:

```python
DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",       # ← your MySQL username
    "password": "your_pass",  # ← your MySQL password
    "database": "expense_tracker",
}
```

### Step 4 — Launch the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` in your browser.

---

## 🗄️ Database Schema

| Table       | Purpose                              |
|-------------|--------------------------------------|
| `users`     | User profile & monthly budget        |
| `categories`| Expense categories (with emoji/color)|
| `expenses`  | All expense records                  |
| `income`    | Income records                       |
| `budgets`   | Per-category monthly budgets         |

---

## ✨ Features

| Page          | Operations |
|---------------|------------|
| 🏠 Dashboard  | KPI cards, budget progress, 30-day trend, category donut, recent transactions |
| ➕ Add Expense| CREATE — add expense with title, amount, category, date, payment mode |
| 📋 View       | READ — filter by date range, category, keyword; download CSV |
| ✏️ Edit/Delete| UPDATE & DELETE — select any expense, edit fields or delete |
| 💰 Income     | CREATE/READ/DELETE income records |
| 📊 Analytics  | Charts: category bar, monthly bar, pie, payment mode breakdown |
| 🎯 Budgets    | Set per-category monthly budgets; visual progress bars |
| ⚙️ Settings   | Update monthly budget; add custom categories |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** — UI framework
- **MySQL + mysql-connector-python** — database & connectivity
- **Pandas** — data manipulation
- **Plotly** — interactive charts

---

## 💡 Notes

- The default user (`default_user`) is seeded automatically by the SQL file.
- `DEFAULT_USER_ID = 1` in `config.py` refers to this user.
- To support multiple users, extend the `users` table and add a login page.
