# # ============================================================
# #  app.py  –  SpendWise Expense Tracker  (Streamlit UI)
# #  Run with:  streamlit run app.py
# # ============================================================

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# from datetime import date, datetime, timedelta
# import calendar

# from config import APP_TITLE, CURRENCY, DEFAULT_USER_ID
# import db_operations as db

# # ── Page config ───────────────────────────────────────────
# st.set_page_config(
#     page_title="SpendWise",
#     page_icon="💸",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ── Custom CSS ────────────────────────────────────────────
# st.markdown(
#     """
# <style>
# /* ── Google Fonts ── */
# @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

# html, body, [class*="css"] {
#     font-family: 'DM Sans', sans-serif;
# }

# /* ── Background ── */
# .stApp {
#     background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
#     min-height: 100vh;
# }

# /* ── Sidebar ── */
# [data-testid="stSidebar"] {
#     background: rgba(255,255,255,0.05) !important;
#     backdrop-filter: blur(20px);
#     border-right: 1px solid rgba(255,255,255,0.1);
# }
# [data-testid="stSidebar"] * { color: #e0e0f0 !important; }

# /* ── Headings ── */
# h1, h2, h3 {
#     font-family: 'Syne', sans-serif !important;
#     color: #ffffff !important;
# }

# /* ── KPI cards ── */
# .kpi-card {
#     background: rgba(255,255,255,0.07);
#     border: 1px solid rgba(255,255,255,0.12);
#     border-radius: 20px;
#     padding: 24px 20px;
#     text-align: center;
#     backdrop-filter: blur(10px);
#     transition: transform 0.2s;
# }
# .kpi-card:hover { transform: translateY(-3px); }
# .kpi-value {
#     font-family: 'Syne', sans-serif;
#     font-size: 2rem;
#     font-weight: 800;
#     color: #a78bfa;
# }
# .kpi-label {
#     font-size: 0.78rem;
#     color: #94a3b8;
#     text-transform: uppercase;
#     letter-spacing: 1px;
#     margin-top: 4px;
# }

# /* ── Section titles ── */
# .section-title {
#     font-family: 'Syne', sans-serif;
#     font-size: 1.3rem;
#     font-weight: 700;
#     color: #e2e8f0;
#     padding: 8px 0 4px;
#     border-bottom: 2px solid #6d28d9;
#     margin-bottom: 18px;
# }

# /* ── Tables ── */
# .stDataFrame { border-radius: 14px; overflow: hidden; }
# [data-testid="stDataFrame"] th {
#     background: #1e1b4b !important;
#     color: #a78bfa !important;
#     font-family: 'Syne', sans-serif !important;
# }

# /* ── Inputs & selects ── */
# .stTextInput > div > div > input,
# .stNumberInput > div > div > input,
# .stSelectbox > div > div,
# .stDateInput > div > div > input,
# .stTextArea textarea {
#     background: rgba(255,255,255,0.08) !important;
#     border: 1px solid rgba(167,139,250,0.4) !important;
#     border-radius: 10px !important;
#     color: #e2e8f0 !important;
# }

# /* ── Buttons ── */
# .stButton > button {
#     background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
#     color: white !important;
#     border: none !important;
#     border-radius: 12px !important;
#     font-family: 'Syne', sans-serif !important;
#     font-weight: 600 !important;
#     padding: 10px 28px !important;
#     transition: all 0.2s !important;
# }
# .stButton > button:hover {
#     transform: translateY(-2px);
#     box-shadow: 0 8px 24px rgba(124,58,237,0.45) !important;
# }

# /* ── Alerts ── */
# .stSuccess { background: rgba(16,185,129,0.15) !important; border-left: 4px solid #10b981 !important; }
# .stError   { background: rgba(239,68,68,0.15)  !important; border-left: 4px solid #ef4444 !important; }
# .stWarning { background: rgba(245,158,11,0.15) !important; border-left: 4px solid #f59e0b !important; }

# /* ── Metric delta text ── */
# [data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

# /* ── Radio / tabs ── */
# .stRadio label { color: #cbd5e1 !important; }
# div[data-baseweb="tab-list"] { background: rgba(255,255,255,0.05) !important; border-radius: 12px !important; }
# div[data-baseweb="tab"]      { color: #94a3b8 !important; }
# div[data-baseweb="tab"][aria-selected="true"] { color: #a78bfa !important; }

# /* General text */
# p, label, .stMarkdown { color: #cbd5e1 !important; }
# </style>
# """,
#     unsafe_allow_html=True,
# )

# # ── Helpers ───────────────────────────────────────────────
# def fmt(amount: float) -> str:
#     return f"{CURRENCY}{amount:,.2f}"


# def plotly_layout(fig, title=""):
#     fig.update_layout(
#         title=dict(text=title, font=dict(family="Syne", size=16, color="#e2e8f0")),
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(0,0,0,0)",
#         font=dict(family="DM Sans", color="#94a3b8"),
#         legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#cbd5e1")),
#         margin=dict(l=20, r=20, t=50, b=20),
#     )
#     fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)")
#     fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)")
#     return fig


# ACCENT_PALETTE = [
#     "#7c3aed","#4f46e5","#0ea5e9","#10b981",
#     "#f59e0b","#ef4444","#ec4899","#8b5cf6",
#     "#14b8a6","#f97316","#06b6d4","#a3e635",
# ]

# # ── Sidebar navigation ────────────────────────────────────
# with st.sidebar:
#     st.markdown(
#         "<h1 style='font-size:1.8rem;margin-bottom:0'>💸 SpendWise</h1>"
#         "<p style='font-size:0.75rem;color:#6d28d9;margin-top:2px;letter-spacing:2px'>EXPENSE TRACKER</p>",
#         unsafe_allow_html=True,
#     )
#     st.divider()

#     page = st.radio(
#         "Navigate",
#         ["🏠 Dashboard", "➕ Add Expense", "📋 View Expenses",
#          "✏️ Edit / Delete", "💰 Income", "📊 Analytics", "🎯 Budgets", "⚙️ Settings"],
#         label_visibility="collapsed",
#     )

#     st.divider()
#     user = db.get_user(DEFAULT_USER_ID)
#     if user:
#         st.markdown(f"**👤 {user['username']}**")
#         st.caption(f"Budget: {fmt(user['monthly_budget'])}/mo")


# # ╔══════════════════════════════════════════════════════════╗
# #   PAGE: DASHBOARD
# # ╚══════════════════════════════════════════════════════════╝
# if page == "🏠 Dashboard":
#     st.markdown("<h1>Dashboard</h1>", unsafe_allow_html=True)

#     summary = db.get_dashboard_summary(DEFAULT_USER_ID)
#     user    = db.get_user(DEFAULT_USER_ID)
#     budget  = float(user["monthly_budget"]) if user else 0

#     # ── KPI row ───────────────────────────────────────────
#     c1, c2, c3, c4, c5 = st.columns(5)
#     kpis = [
#         (c1, fmt(summary["monthly_expense"]), "This Month's Spend"),
#         (c2, fmt(summary["monthly_income"]),  "This Month's Income"),
#         (c3, fmt(max(summary["savings"], 0)), "Savings"),
#         (c4, str(summary["txn_count"]),        "Transactions"),
#         (c5, fmt(summary["all_time"]),          "All-Time Spent"),
#     ]
#     for col, val, label in kpis:
#         col.markdown(
#             f"<div class='kpi-card'>"
#             f"<div class='kpi-value'>{val}</div>"
#             f"<div class='kpi-label'>{label}</div>"
#             f"</div>",
#             unsafe_allow_html=True,
#         )

#     st.markdown("<br>", unsafe_allow_html=True)

#     # ── Budget progress bar ───────────────────────────────
#     if budget > 0:
        
#         pct = min(summary["monthly_expense"] / budget * 100, 100)
#         color = "#10b981" if pct < 70 else ("#f59e0b" if pct < 90 else "#ef4444")
#         st.markdown(
#             f"<div style='background:rgba(255,255,255,0.07);border-radius:16px;padding:20px'>"
#             f"<p style='margin:0 0 8px;font-weight:600'>Monthly Budget Usage — {pct:.1f}%</p>"
#             f"<div style='background:rgba(255,255,255,0.1);border-radius:99px;height:14px'>"
#             f"<div style='background:{color};width:{pct}%;height:14px;border-radius:99px;"
#             f"transition:width 0.6s'></div></div>"
#             f"<p style='margin:6px 0 0;font-size:0.82rem;color:#94a3b8'>"
#             f"Spent {fmt(summary['monthly_expense'])} of {fmt(budget)}</p>"
#             f"</div>",
#             unsafe_allow_html=True,
#         )
#         st.markdown("<br>", unsafe_allow_html=True)

#     # ── Charts row ────────────────────────────────────────
#     col_left, col_right = st.columns([3, 2])

#     with col_left:
#         st.markdown("<div class='section-title'>Spending Trend (30 days)</div>", unsafe_allow_html=True)
#         daily = db.get_daily_expenses(DEFAULT_USER_ID, days=30)
#         if daily:
#             df_daily = pd.DataFrame(daily)
#             df_daily["day"] = pd.to_datetime(df_daily["day"])
#             fig = go.Figure()
#             fig.add_trace(go.Scatter(
#                 x=df_daily["day"], y=df_daily["total"],
#                 mode="lines+markers",
#                 line=dict(color="#7c3aed", width=2.5),
#                 marker=dict(size=6, color="#a78bfa"),
#                 fill="tozeroy",
#                 fillcolor="rgba(124,58,237,0.12)",
#                 name="Daily Spend",
#             ))
#             plotly_layout(fig)
#             st.plotly_chart(fig, use_container_width=True)
#         else:
#             st.info("No expense data yet. Add some expenses to see the trend!")

#     with col_right:
#         st.markdown("<div class='section-title'>By Category (This Month)</div>", unsafe_allow_html=True)
#         today = date.today()
#         cat_data = db.get_category_totals(
#             DEFAULT_USER_ID,
#             date(today.year, today.month, 1),
#             today,
#         )
#         if cat_data:
#             df_cat = pd.DataFrame(cat_data)
#             fig2 = px.pie(
#                 df_cat, names="category", values="total",
#                 hole=0.55,
#                 color_discrete_sequence=ACCENT_PALETTE,
#             )
#             fig2.update_traces(textinfo="percent+label", textfont_size=11)
#             plotly_layout(fig2)
#             st.plotly_chart(fig2, use_container_width=True)
#         else:
#             st.info("No data for this month yet.")

#     # ── Recent transactions ───────────────────────────────
#     st.markdown("<div class='section-title'>Recent Transactions</div>", unsafe_allow_html=True)
#     recent = db.get_expenses(DEFAULT_USER_ID, limit=8)
#     if recent:
#         for exp in recent:
#             c1, c2, c3, c4 = st.columns([0.5, 3, 1.5, 1.5])
#             c1.markdown(f"<span style='font-size:1.5rem'>{exp['category_icon']}</span>", unsafe_allow_html=True)
#             c2.markdown(f"**{exp['title']}**  \n<span style='font-size:0.78rem;color:#64748b'>{exp['category']} · {exp['expense_date']}</span>", unsafe_allow_html=True)
#             c3.markdown(f"<span style='color:#a78bfa;font-weight:600'>{fmt(float(exp['amount']))}</span>", unsafe_allow_html=True)
#             c4.markdown(f"<span style='font-size:0.78rem;color:#64748b'>{exp['payment_mode']}</span>", unsafe_allow_html=True)
#             st.divider()
#     else:
#         st.info("No transactions yet.")


# # ╔══════════════════════════════════════════════════════════╗
# #   PAGE: ADD EXPENSE
# # ╚══════════════════════════════════════════════════════════╝
# elif page == "➕ Add Expense":
#     st.markdown("<h1>Add Expense</h1>", unsafe_allow_html=True)

#     categories = db.get_all_categories()
#     cat_map = {f"{c['icon']} {c['name']}": c["id"] for c in categories}

#     with st.form("add_expense_form", clear_on_submit=True):
#         c1, c2 = st.columns(2)
#         title   = c1.text_input("Title *", placeholder="e.g. Dinner at restaurant")
#         amount  = c2.number_input("Amount (₹) *", min_value=0.01, step=10.0, format="%.2f")

#         c3, c4, c5 = st.columns(3)
#         cat_label   = c3.selectbox("Category *", list(cat_map.keys()))
#         exp_date    = c4.date_input("Date *", value=date.today())
#         payment     = c5.selectbox("Payment Mode", ["Cash","Card","UPI","Net Banking","Other"])

#         desc        = st.text_area("Description (optional)", height=90)

#         submitted = st.form_submit_button("💾 Save Expense", use_container_width=True)

#     if submitted:
#         if not title:
#             st.error("Title is required.")
#         elif amount <= 0:
#             st.error("Amount must be greater than 0.")
#         else:
#             ok = db.add_expense(
#                 title=title, amount=amount,
#                 category_id=cat_map[cat_label],
#                 expense_date=exp_date,
#                 description=desc, payment_mode=payment,
#             )
#             if ok:
#                 st.success(f"✅ Expense **{title}** ({fmt(amount)}) saved!")
#                 st.balloons()


# # ╔══════════════════════════════════════════════════════════╗
# #   PAGE: VIEW EXPENSES
# # ╚══════════════════════════════════════════════════════════╝
# elif page == "📋 View Expenses":
#     st.markdown("<h1>View Expenses</h1>", unsafe_allow_html=True)

#     # Filters
#     with st.expander("🔍 Filters", expanded=True):
#         fc1, fc2, fc3, fc4 = st.columns(4)
#         start = fc1.date_input("From", value=date.today().replace(day=1))
#         end   = fc2.date_input("To",   value=date.today())

#         categories  = db.get_all_categories()
#         cat_options = {"All": None} | {f"{c['icon']} {c['name']}": c["id"] for c in categories}
#         cat_sel     = fc3.selectbox("Category", list(cat_options.keys()))
#         search_q    = fc4.text_input("Search", placeholder="keyword…")

#     expenses = db.get_expenses(
#         DEFAULT_USER_ID,
#         start_date=start, end_date=end,
#         category_id=cat_options[cat_sel],
#         search=search_q,
#     )

#     if expenses:
#         df = pd.DataFrame(expenses)
#         total = df["amount"].astype(float).sum()
#         st.markdown(
#             f"<p>Showing <b>{len(df)}</b> transactions — Total: "
#             f"<b style='color:#a78bfa'>{fmt(total)}</b></p>",
#             unsafe_allow_html=True,
#         )
#         display_cols = ["expense_date","category_icon","category","title","amount","payment_mode","description"]
#         display_cols = [c for c in display_cols if c in df.columns]
#         st.dataframe(
#             df[display_cols].rename(columns={
#                 "expense_date":"Date","category_icon":"","category":"Category",
#                 "title":"Title","amount":"Amount (₹)","payment_mode":"Mode","description":"Description",
#             }),
#             use_container_width=True, hide_index=True,
#         )

#         # Download CSV
#         csv = df.to_csv(index=False).encode()
#         st.download_button("⬇️ Download CSV", csv, "expenses.csv", "text/csv")
#     else:
#         st.info("No expenses found for the selected filters.")


# # ╔══════════════════════════════════════════════════════════╗
# #   PAGE: EDIT / DELETE
# # ╚══════════════════════════════════════════════════════════╝
# elif page == "✏️ Edit / Delete":
#     st.markdown("<h1>Edit / Delete Expense</h1>", unsafe_allow_html=True)

#     expenses = db.get_expenses(DEFAULT_USER_ID, limit=200)
#     if not expenses:
#         st.info("No expenses to edit.")
#     else:
#         options = {f"[{e['expense_date']}] {e['title']} — {fmt(float(e['amount']))}": e["id"] for e in expenses}
#         selected_label = st.selectbox("Select an expense", list(options.keys()))
#         expense_id = options[selected_label]
#         row = db.get_expense_by_id(expense_id)

#         if row:
#             categories = db.get_all_categories()
#             cat_map    = {f"{c['icon']} {c['name']}": c["id"] for c in categories}
#             cat_rev    = {c["id"]: f"{c['icon']} {c['name']}" for c in categories}
#             cur_cat    = cat_rev.get(row["category_id"], list(cat_map.keys())[0])

#             tab_edit, tab_del = st.tabs(["✏️ Edit", "🗑️ Delete"])

#             with tab_edit:
#                 with st.form("edit_form"):
#                     c1, c2 = st.columns(2)
#                     new_title  = c1.text_input("Title",  value=row["title"])
#                     new_amount = c2.number_input("Amount", value=float(row["amount"]), min_value=0.01, step=10.0)

#                     c3, c4, c5 = st.columns(3)
#                     new_cat  = c3.selectbox("Category", list(cat_map.keys()),
#                                             index=list(cat_map.keys()).index(cur_cat))
#                     new_date = c4.date_input("Date", value=row["expense_date"])
#                     new_mode = c5.selectbox("Payment Mode",
#                                             ["Cash","Card","UPI","Net Banking","Other"],
#                                             index=["Cash","Card","UPI","Net Banking","Other"].index(row["payment_mode"]))
#                     new_desc = st.text_area("Description", value=row["description"] or "")

#                     if st.form_submit_button("💾 Update Expense", use_container_width=True):
#                         ok = db.update_expense(
#                             expense_id=expense_id,
#                             title=new_title, amount=new_amount,
#                             category_id=cat_map[new_cat],
#                             expense_date=new_date, description=new_desc,
#                             payment_mode=new_mode,
#                         )
#                         if ok:
#                             st.success("✅ Expense updated!")

#             with tab_del:
#                 st.warning(f"You are about to delete **{row['title']}** ({fmt(float(row['amount']))}). This cannot be undone.")
#                 if st.button("🗑️ Confirm Delete", type="primary"):
#                     if db.delete_expense(expense_id):
#                         st.success("Expense deleted.")
#                         st.rerun()


# # ╔══════════════════════════════════════════════════════════╗
# #   PAGE: INCOME
# # ╚══════════════════════════════════════════════════════════╝
# elif page == "💰 Income":
#     st.markdown("<h1>Income</h1>", unsafe_allow_html=True)

#     tab_add, tab_view = st.tabs(["➕ Add Income", "📋 View Income"])

#     with tab_add:
#         with st.form("add_income_form", clear_on_submit=True):
#             c1, c2 = st.columns(2)
#             source = c1.text_input("Source *", placeholder="e.g. Salary, Freelance")
#             amount = c2.number_input("Amount (₹) *", min_value=0.01, step=100.0, format="%.2f")
#             c3, c4 = st.columns(2)
#             inc_date = c3.date_input("Date *", value=date.today())
#             desc     = c4.text_input("Description (optional)")
#             if st.form_submit_button("💾 Save Income", use_container_width=True):
#                 if not source:
#                     st.error("Source is required.")
#                 else:
#                     ok = db.add_income(source, amount, inc_date, desc)
#                     if ok: st.success(f"✅ Income from **{source}** ({fmt(amount)}) added!")

#     with tab_view:
#         fc1, fc2 = st.columns(2)
#         start = fc1.date_input("From", value=date.today().replace(day=1), key="inc_start")
#         end   = fc2.date_input("To",   value=date.today(),               key="inc_end")
#         income_rows = db.get_income(DEFAULT_USER_ID, start, end)
#         if income_rows:
#             df_inc = pd.DataFrame(income_rows)
#             total_inc = df_inc["amount"].astype(float).sum()
#             st.markdown(f"**Total Income: <span style='color:#10b981'>{fmt(total_inc)}</span>**", unsafe_allow_html=True)
#             st.dataframe(df_inc[["income_date","source","amount","description"]].rename(
#                 columns={"income_date":"Date","source":"Source","amount":"Amount (₹)","description":"Description"}
#             ), use_container_width=True, hide_index=True)

#             col_del, _ = st.columns([1, 3])
#             del_id = col_del.number_input("Delete Income ID", min_value=1, step=1)
#             if st.button("🗑️ Delete"):
#                 if db.delete_income(del_id):
#                     st.success("Deleted."); st.rerun()
#         else:
#             st.info("No income records found.")


# # ╔══════════════════════════════════════════════════════════╗
# #   PAGE: ANALYTICS
# # ╚══════════════════════════════════════════════════════════╝
# elif page == "📊 Analytics":
#     st.markdown("<h1>Analytics</h1>", unsafe_allow_html=True)

#     # Date range selector
#     col_a, col_b = st.columns(2)
#     a_start = col_a.date_input("From", value=date.today() - timedelta(days=90), key="an_start")
#     a_end   = col_b.date_input("To",   value=date.today(),                       key="an_end")

#     cat_totals   = db.get_category_totals(DEFAULT_USER_ID, a_start, a_end)
#     monthly_tots = db.get_monthly_totals(DEFAULT_USER_ID, months=12)
#     payment_data = db.get_payment_mode_summary(DEFAULT_USER_ID)

#     # ── Row 1: Category bar + Monthly trend ───────────────
#     r1c1, r1c2 = st.columns(2)

#     with r1c1:
#         st.markdown("<div class='section-title'>Spending by Category</div>", unsafe_allow_html=True)
#         if cat_totals:
#             df_cat = pd.DataFrame(cat_totals)
#             fig = px.bar(
#                 df_cat, x="total", y="category", orientation="h",
#                 color="category", color_discrete_sequence=ACCENT_PALETTE,
#                 text="total",
#             )
#             fig.update_traces(texttemplate=f"₹%{{x:,.0f}}", textposition="outside")
#             plotly_layout(fig)
#             st.plotly_chart(fig, use_container_width=True)
#         else:
#             st.info("No data for this range.")

#     with r1c2:
#         st.markdown("<div class='section-title'>Monthly Spending Trend</div>", unsafe_allow_html=True)
#         if monthly_tots:
#             df_m = pd.DataFrame(monthly_tots)
#             fig2 = go.Figure(go.Bar(
#                 x=df_m["month"], y=df_m["total"].astype(float),
#                 marker_color=ACCENT_PALETTE[0],
#                 marker_line_color="rgba(255,255,255,0.1)",
#                 marker_line_width=1,
#             ))
#             plotly_layout(fig2)
#             st.plotly_chart(fig2, use_container_width=True)
#         else:
#             st.info("Not enough data.")

#     # ── Row 2: Pie + Payment mode ─────────────────────────
#     r2c1, r2c2 = st.columns(2)

#     with r2c1:
#         st.markdown("<div class='section-title'>Category Distribution</div>", unsafe_allow_html=True)
#         if cat_totals:
#             df_cat2 = pd.DataFrame(cat_totals)
#             fig3 = px.pie(df_cat2, names="category", values="total",
#                           color_discrete_sequence=ACCENT_PALETTE, hole=0.4)
#             fig3.update_traces(textinfo="percent+label")
#             plotly_layout(fig3)
#             st.plotly_chart(fig3, use_container_width=True)

#     with r2c2:
#         st.markdown("<div class='section-title'>Payment Mode Breakdown</div>", unsafe_allow_html=True)
#         if payment_data:
#             df_pay = pd.DataFrame(payment_data)
#             fig4 = px.bar(df_pay, x="payment_mode", y="total",
#                           color="payment_mode", color_discrete_sequence=ACCENT_PALETTE,
#                           text="cnt")
#             fig4.update_traces(texttemplate="%{text} txns", textposition="outside")
#             plotly_layout(fig4)
#             st.plotly_chart(fig4, use_container_width=True)

#     # ── Summary table ─────────────────────────────────────
#     if cat_totals:
#         st.markdown("<div class='section-title'>Category Summary Table</div>", unsafe_allow_html=True)
#         df_sum = pd.DataFrame(cat_totals)
#         df_sum["total"] = df_sum["total"].apply(lambda x: fmt(float(x)))
#         st.dataframe(df_sum[["icon","category","total","txn_count"]].rename(
#             columns={"icon":"","category":"Category","total":"Total Spent","txn_count":"Transactions"}
#         ), use_container_width=True, hide_index=True)


# # ╔══════════════════════════════════════════════════════════╗
# #   PAGE: BUDGETS
# # ╚══════════════════════════════════════════════════════════╝
# elif page == "🎯 Budgets":
#     st.markdown("<h1>Category Budgets</h1>", unsafe_allow_html=True)

#     month_year = st.text_input("Month (YYYY-MM)", value=date.today().strftime("%Y-%m"))

#     # Set budget form
#     with st.expander("➕ Set / Update a Category Budget"):
#         categories = db.get_all_categories()
#         cat_map    = {f"{c['icon']} {c['name']}": c["id"] for c in categories}
#         with st.form("budget_form", clear_on_submit=True):
#             c1, c2 = st.columns(2)
#             cat_lbl = c1.selectbox("Category", list(cat_map.keys()))
#             bud_amt = c2.number_input("Budget (₹)", min_value=0.0, step=500.0, format="%.2f")
#             if st.form_submit_button("💾 Save Budget", use_container_width=True):
#                 ok = db.set_budget(DEFAULT_USER_ID, cat_map[cat_lbl], month_year, bud_amt)
#                 if ok: st.success("Budget saved!"); st.rerun()

#     # Budget vs Actual
#     budgets = db.get_budgets(DEFAULT_USER_ID, month_year)
#     if budgets:
#         st.markdown("<div class='section-title'>Budget vs Actual</div>", unsafe_allow_html=True)
#         for b in budgets:
#             spent  = float(b["spent"])
#             budget = float(b["budget_amt"])
#             pct    = min(spent / budget * 100, 100) if budget > 0 else 0
#             color  = "#10b981" if pct < 70 else ("#f59e0b" if pct < 90 else "#ef4444")
#             st.markdown(
#                 f"<div style='background:rgba(255,255,255,0.05);border-radius:14px;padding:16px;margin-bottom:10px'>"
#                 f"<div style='display:flex;justify-content:space-between'>"
#                 f"<span>{b['icon']} <b>{b['category']}</b></span>"
#                 f"<span style='color:#94a3b8'>{fmt(spent)} / {fmt(budget)}</span></div>"
#                 f"<div style='background:rgba(255,255,255,0.08);border-radius:99px;height:10px;margin-top:8px'>"
#                 f"<div style='background:{color};width:{pct:.1f}%;height:10px;border-radius:99px'></div></div>"
#                 f"<p style='margin:4px 0 0;font-size:0.75rem;color:#64748b'>{pct:.1f}% used</p>"
#                 f"</div>",
#                 unsafe_allow_html=True,
#             )

#         # Gauge chart: top 5
#         df_b = pd.DataFrame(budgets)
#         df_b["pct"] = (df_b["spent"].astype(float) / df_b["budget_amt"].astype(float).replace(0,1) * 100).clip(0,100)
#         top5 = df_b.nlargest(5, "pct")
#         fig = px.bar(top5, x="pct", y="category", orientation="h",
#                      color="pct", color_continuous_scale=["#10b981","#f59e0b","#ef4444"],
#                      range_color=[0,100], text="pct")
#         fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
#         plotly_layout(fig, "Budget Usage % (Top 5)")
#         st.plotly_chart(fig, use_container_width=True)
#     else:
#         st.info(f"No budgets set for {month_year}. Use the form above to add some!")


# # ╔══════════════════════════════════════════════════════════╗
# #   PAGE: SETTINGS
# # ╚══════════════════════════════════════════════════════════╝
# elif page == "⚙️ Settings":
#     st.markdown("<h1>Settings</h1>", unsafe_allow_html=True)

#     user = db.get_user(DEFAULT_USER_ID)
#     if user:
#         st.subheader("Monthly Budget")
#         new_budget = st.number_input(
#             "Set Monthly Budget (₹)",
#             value=float(user["monthly_budget"]),
#             min_value=0.0, step=1000.0, format="%.2f",
#         )
#         if st.button("💾 Update Budget"):
#             if db.update_monthly_budget(DEFAULT_USER_ID, new_budget):
#                 st.success("Budget updated!")

#     st.divider()
#     st.subheader("Add Custom Category")
#     with st.form("cat_form", clear_on_submit=True):
#         cc1, cc2, cc3 = st.columns(3)
#         cat_name  = cc1.text_input("Category Name")
#         cat_icon  = cc2.text_input("Emoji Icon", value="💰")
#         cat_color = cc3.color_picker("Color", value="#6C63FF")
#         if st.form_submit_button("➕ Add Category", use_container_width=True):
#             if cat_name:
#                 ok = db.add_category(cat_name, cat_icon, cat_color)
#                 if ok: st.success(f"Category '{cat_name}' added!")
#             else:
#                 st.error("Category name cannot be empty.")

#     st.divider()
#     st.subheader("All Categories")
#     cats = db.get_all_categories()
#     df_cats = pd.DataFrame(cats)[["icon","name","color"]] if cats else pd.DataFrame()
#     if not df_cats.empty:
#         st.dataframe(df_cats.rename(columns={"icon":"","name":"Name","color":"Color"}),
#                      use_container_width=True, hide_index=True)
