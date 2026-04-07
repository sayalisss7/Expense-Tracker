# ============================================================
#  db_operations.py  –  All CRUD operations for Expense Tracker
# ============================================================

from mysql.connector import Error
from config import get_cursor, DEFAULT_USER_ID
from datetime import date, datetime



# ╔══════════════════════════════════════════════════════════╗
#  CATEGORIES
# ╚══════════════════════════════════════════════════════════╝

def get_all_categories() -> list[dict]:
    """Fetch every category row."""
    conn, cur = get_cursor()
    cur.execute("SELECT * FROM categories ORDER BY name")
    rows = cur.fetchall()
    cur.close()
    return rows


def add_category(name: str, icon: str = "💰", color: str = "#6C63FF") -> bool:
    """INSERT a new category. Returns True on success."""
    conn, cur = get_cursor()
    try:
        cur.execute(
            "INSERT INTO categories (name, icon, color) VALUES (%s, %s, %s)",
            (name.strip(), icon, color),
        )
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
       
        return False
    finally:
        cur.close()


# ╔══════════════════════════════════════════════════════════╗
#  EXPENSES  –  Create / Read / Update / Delete
# ╚══════════════════════════════════════════════════════════╝

def add_expense(
    title: str,
    amount: float,
    category_id: int,
    expense_date: date,
    description: str = "",
    payment_mode: str = "Cash",
    user_id: int = DEFAULT_USER_ID,
) -> bool:
    """INSERT a new expense row."""
    conn, cur = get_cursor()
    sql = """
        INSERT INTO expenses
            (user_id, category_id, title, amount, expense_date, description, payment_mode)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cur.execute(sql, (user_id, category_id, title.strip(), amount,
                          expense_date, description.strip(), payment_mode))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
     
        return False
    finally:
        cur.close()


def get_expenses(
    user_id: int = DEFAULT_USER_ID,
    start_date: date | None = None,
    end_date: date | None = None,
    category_id: int | None = None,
    search: str = "",
    limit: int = 500,
) -> list[dict]:
    """SELECT expenses with optional filters."""
    conn, cur = get_cursor()
    sql = """
        SELECT e.id, c.name AS category, c.icon AS category_icon, c.color AS category_color,
               e.title, e.amount, e.expense_date, e.description, e.payment_mode, e.created_at
        FROM   expenses e
        JOIN   categories c ON e.category_id = c.id
        WHERE  e.user_id = %s
    """
    params: list = [user_id]

    if start_date:
        sql += " AND e.expense_date >= %s"
        params.append(start_date)
    if end_date:
        sql += " AND e.expense_date <= %s"
        params.append(end_date)
    if category_id:
        sql += " AND e.category_id = %s"
        params.append(category_id)
    if search:
        sql += " AND (e.title LIKE %s OR e.description LIKE %s)"
        params += [f"%{search}%", f"%{search}%"]

    sql += " ORDER BY e.expense_date DESC, e.created_at DESC LIMIT %s"
    params.append(limit)

    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    return rows


def get_expense_by_id(expense_id: int) -> dict | None:
    """Fetch a single expense row (with category join)."""
    conn, cur = get_cursor()
    cur.execute(
        """
        SELECT e.*, c.name AS category_name, c.id AS category_id
        FROM   expenses e
        JOIN   categories c ON e.category_id = c.id
        WHERE  e.id = %s
        """,
        (expense_id,),
    )
    row = cur.fetchone()
    cur.close()
    return row


def update_expense(
    expense_id: int,
    title: str,
    amount: float,
    category_id: int,
    expense_date: date,
    description: str,
    payment_mode: str,
) -> bool:
    """UPDATE an existing expense row."""
    conn, cur = get_cursor()
    sql = """
        UPDATE expenses
        SET title=%s, amount=%s, category_id=%s,
            expense_date=%s, description=%s, payment_mode=%s
        WHERE id=%s
    """
    try:
        cur.execute(sql, (title.strip(), amount, category_id,
                          expense_date, description.strip(), payment_mode, expense_id))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
       
        return False
    finally:
        cur.close()


def delete_expense(expense_id: int) -> bool:
    """DELETE an expense row by primary key."""
    conn, cur = get_cursor()
    try:
        cur.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        
        return False
    finally:
        cur.close()


# ╔══════════════════════════════════════════════════════════╗
#  INCOME
# ╚══════════════════════════════════════════════════════════╝

def add_income(
    source: str,
    amount: float,
    income_date: date,
    description: str = "",
    user_id: int = DEFAULT_USER_ID,
) -> bool:
    conn, cur = get_cursor()
    sql = """
        INSERT INTO income (user_id, source, amount, income_date, description)
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cur.execute(sql, (user_id, source.strip(), amount, income_date, description.strip()))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
      
        return False
    finally:
        cur.close()


def get_income(
    user_id: int = DEFAULT_USER_ID,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[dict]:
    conn, cur = get_cursor()
    sql = "SELECT * FROM income WHERE user_id = %s"
    params: list = [user_id]
    if start_date:
        sql += " AND income_date >= %s"; params.append(start_date)
    if end_date:
        sql += " AND income_date <= %s"; params.append(end_date)
    sql += " ORDER BY income_date DESC"
    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    return rows


def delete_income(income_id: int) -> bool:
    conn, cur = get_cursor()
    try:
        cur.execute("DELETE FROM income WHERE id = %s", (income_id,))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
       
        return False
    finally:
        cur.close()


# ╔══════════════════════════════════════════════════════════╗
#  BUDGETS
# ╚══════════════════════════════════════════════════════════╝

def set_budget(user_id: int, category_id: int, month_year: str, amount: float) -> bool:
    """INSERT or UPDATE a monthly category budget."""
    conn, cur = get_cursor()
    sql = """
        INSERT INTO budgets (user_id, category_id, month_year, budget_amt)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE budget_amt = VALUES(budget_amt)
    """
    try:
        cur.execute(sql, (user_id, category_id, month_year, amount))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
      
        return False
    finally:
        cur.close()


def get_budgets(user_id: int = DEFAULT_USER_ID, month_year: str | None = None) -> list[dict]:
    conn, cur = get_cursor()
    sql = """
        SELECT b.id, c.name AS category, c.icon, b.month_year, b.budget_amt,
               COALESCE(SUM(e.amount), 0) AS spent
        FROM   budgets b
        JOIN   categories c ON b.category_id = c.id
        LEFT JOIN expenses e
               ON  e.category_id = b.category_id
               AND e.user_id     = b.user_id
               AND DATE_FORMAT(e.expense_date, '%%Y-%%m') = b.month_year
        WHERE  b.user_id = %s
    """
    params: list = [user_id]
    if month_year:
        sql += " AND b.month_year = %s"
        params.append(month_year)
    sql += " GROUP BY b.id, c.name, c.icon, b.month_year, b.budget_amt"
    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    return rows


# ╔══════════════════════════════════════════════════════════╗
#  ANALYTICS QUERIES
# ╚══════════════════════════════════════════════════════════╝

def get_monthly_totals(user_id: int = DEFAULT_USER_ID, months: int = 12) -> list[dict]:
    """Monthly total expenses for the last `months` months."""
    conn, cur = get_cursor()
    cur.execute(
        """
        SELECT DATE_FORMAT(expense_date, '%%Y-%%m') AS month,
               SUM(amount)                          AS total
        FROM   expenses
        WHERE  user_id = %s
          AND  expense_date >= DATE_SUB(CURDATE(), INTERVAL %s MONTH)
        GROUP  BY month
        ORDER  BY month
        """,
        (user_id, months),
    )
    rows = cur.fetchall()
    cur.close()
    return rows


def get_category_totals(
    user_id: int = DEFAULT_USER_ID,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[dict]:
    """Total spending grouped by category for a date range."""
    conn, cur = get_cursor()
    sql = """
        SELECT c.name AS category, c.icon, c.color,
               SUM(e.amount) AS total, COUNT(*) AS txn_count
        FROM   expenses e
        JOIN   categories c ON e.category_id = c.id
        WHERE  e.user_id = %s
    """
    params: list = [user_id]
    if start_date:
        sql += " AND e.expense_date >= %s"; params.append(start_date)
    if end_date:
        sql += " AND e.expense_date <= %s"; params.append(end_date)
    sql += " GROUP BY c.id, c.name, c.icon, c.color ORDER BY total DESC"
    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    return rows


def get_dashboard_summary(user_id: int = DEFAULT_USER_ID) -> dict:
    """Key KPIs for the current month dashboard."""
    conn, cur = get_cursor()

    # Current month expenses
    cur.execute(
        """
        SELECT COALESCE(SUM(amount), 0) AS total_expense,
               COUNT(*)                 AS txn_count
        FROM   expenses
        WHERE  user_id = %s
          AND  YEAR(expense_date)  = YEAR(CURDATE())
          AND  MONTH(expense_date) = MONTH(CURDATE())
        """,
        (user_id,),
    )
    exp = cur.fetchone()

    # Current month income
    cur.execute(
        """
        SELECT COALESCE(SUM(amount), 0) AS total_income
        FROM   income
        WHERE  user_id = %s
          AND  YEAR(income_date)  = YEAR(CURDATE())
          AND  MONTH(income_date) = MONTH(CURDATE())
        """,
        (user_id,),
    )
    inc = cur.fetchone()

    # All-time totals
    cur.execute(
        "SELECT COALESCE(SUM(amount), 0) AS all_time FROM expenses WHERE user_id=%s",
        (user_id,),
    )
    all_time = cur.fetchone()

    cur.close()
    return {
        "monthly_expense": float(exp["total_expense"]),
        "monthly_income":  float(inc["total_income"]),
        "txn_count":       int(exp["txn_count"]),
        "savings":         float(inc["total_income"]) - float(exp["total_expense"]),
        "all_time":        float(all_time["all_time"]),
    }


def get_daily_expenses(user_id: int = DEFAULT_USER_ID, days: int = 30) -> list[dict]:
    """Daily totals for the past `days` days (for trend line)."""
    conn, cur = get_cursor()
    cur.execute(
        """
        SELECT expense_date AS day, SUM(amount) AS total
        FROM   expenses
        WHERE  user_id = %s
          AND  expense_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        GROUP  BY expense_date
        ORDER  BY expense_date
        """,
        (user_id, days),
    )
    rows = cur.fetchall()
    cur.close()
    return rows


def get_payment_mode_summary(user_id: int = DEFAULT_USER_ID) -> list[dict]:
    conn, cur = get_cursor()
    cur.execute(
        """
        SELECT payment_mode, SUM(amount) AS total, COUNT(*) AS cnt
        FROM   expenses
        WHERE  user_id = %s
        GROUP  BY payment_mode
        ORDER  BY total DESC
        """,
        (user_id,),
    )
    rows = cur.fetchall()
    cur.close()
    return rows


# ╔══════════════════════════════════════════════════════════╗
#  USER SETTINGS
# ╚══════════════════════════════════════════════════════════╝

def get_user(user_id: int = DEFAULT_USER_ID) -> dict | None:
    conn, cur = get_cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    return row


def update_monthly_budget(user_id: int, budget: float) -> bool:
    conn, cur = get_cursor()
    try:
        cur.execute(
            "UPDATE users SET monthly_budget = %s WHERE id = %s",
            (budget, user_id),
        )
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
      
        return False
    finally:
        cur.close()
