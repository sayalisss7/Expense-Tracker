# ============================================================
#  config.py  –  Database connection & app configuration
# ============================================================

import mysql.connector
from mysql.connector import Error
import streamlit as st

# ── MySQL connection parameters ───────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",          # ← change to your MySQL username
    "password": "Feat@123",          # ← change to your MySQL password
    "database": "expense_tracker",
    "charset":  "utf8mb4",
    "autocommit": False,
}

# ── App-level settings ────────────────────────────────────
APP_TITLE   = "SpendWise 💸"
DEFAULT_USER_ID = 1          # matches the seeded default_user

# Indian Rupee symbol (used throughout the UI)
CURRENCY = "₹"


# ── Connection helper (cached per Streamlit session) ──────
@st.cache_resource(show_spinner=False)
def get_connection():
    """
    Returns a persistent MySQL connection cached for the
    entire Streamlit session.  Recreates it if it dropped.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        st.error(f"❌ Cannot connect to MySQL: {e}")
        st.info(
            "Make sure MySQL is running and your credentials in "
            "`config.py` are correct.  Then run `setup_database.sql`."
        )
        st.stop()


def get_cursor(dictionary: bool = True):
    """
    Returns (connection, cursor).
    Uses `dictionary=True` by default so rows come back as dicts.
    """
    conn = get_connection()
    # Ping and reconnect if the connection timed out
    try:
        conn.ping(reconnect=True, attempts=3, delay=1)
    except Error:
        # Clear cache and try fresh
        get_connection.clear()
        conn = get_connection()
    return conn, conn.cursor(dictionary=dictionary)
