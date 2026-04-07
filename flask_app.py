from flask import Flask, render_template, request, redirect, url_for, flash
import db_operations as db
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "secret123"


# ───────────────── Dashboard ─────────────────
# @app.route("/")
# def dashboard():
#     summary = db.get_dashboard_summary(1)
#     return render_template("dashboard.html", summary=summary)
# from collections import defaultdict

# @app.route("/dashboard")
# def dashboard():
#     expenses = get_all_expenses()   # or your DB function
#     income = get_all_income()       # adjust based on your code

#     total_income = sum(i['amount'] for i in income)
#     total_expense = sum(e['amount'] for e in expenses)

#     # 🔥 Category-wise grouping
#     category_data = defaultdict(float)

#     for e in expenses:
#         category = e['category'] if e['category'] else "Other"
#         category_data[category] += e['amount']

#     chart_labels = list(category_data.keys())
#     chart_values = list(category_data.values())

#     summary = {
#         "monthly_income": total_income,
#         "monthly_expense": total_expense,
#         "savings": total_income - total_expense
#     }

#     return render_template(
#         "dashboard.html",
#         summary=summary,
#         chart_labels=chart_labels,
#         chart_values=chart_values
#     )



# @app.route("/")
# @app.route("/dashboard")
# def dashboard():
#     expenses = db.get_expenses(1)
#     income = db.get_income(1)

#     total_income = sum(i['amount'] for i in income)
#     total_expense = sum(e['amount'] for e in expenses)

#     from collections import defaultdict
#     category_data = defaultdict(float)

    # for e in expenses:
    #     category = e.get('category', "Other")
    #     category_data[category] += e['amount']

    # chart_labels = list(category_data.keys())
    # chart_values = list(category_data.values())

#     from collections import defaultdict

# category_data = defaultdict(float)

# for e in expenses:
#     category = e.get('category', "Other")
#     category_data[category] += float(e['amount'])

# total_income = sum(float(i['amount']) for i in income)
# total_expense = sum(float(e['amount']) for e in expenses)

# summary = {
#         "monthly_income": total_income,
#         "monthly_expense": total_expense,
#         "savings": total_income - total_expense
#     }

# return render_template(
#         "dashboard.html",
#         summary=summary,
#         chart_labels=chart_labels,
#         chart_values=chart_values
#     )
from collections import defaultdict

@app.route("/")
@app.route("/dashboard")
def dashboard():
    expenses = db.get_expenses(1)
    income = db.get_income(1)

    # 🔥 Category-wise grouping
    category_data = defaultdict(float)

    for e in expenses:
        category = e.get('category', "Other")
        category_data[category] += float(e['amount'])

    chart_labels = list(category_data.keys())
    chart_values = list(category_data.values())

    # 💰 Totals
    total_income = sum(float(i['amount']) for i in income)
    total_expense = sum(float(e['amount']) for e in expenses)

    summary = {
        "monthly_income": total_income,
        "monthly_expense": total_expense,
        "savings": total_income - total_expense
    }

    return render_template(
        "dashboard.html",
        summary=summary,
        chart_labels=chart_labels,
        chart_values=chart_values
    )




# ───────────────── Expenses List ─────────────────
@app.route("/expenses")
def expenses():
    data = db.get_expenses(1)

    for e in data:
        e["date"] = e["expense_date"]

    return render_template("expenses.html", expenses=data)


# ───────────────── Add Expense ─────────────────
@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():
    categories = db.get_all_categories()

    if request.method == "POST":
        try:
            title = request.form["title"].strip()
            amount = float(request.form["amount"])
            category_id = int(request.form["category_id"])

            # ✅ FIX DATE
            date_val = request.form["date"]
            if date_val:
                date_val = datetime.strptime(date_val, "%Y-%m-%d").date()
            else:
                date_val = date.today()

            # ✅ FIX PAYMENT MODE
            payment = request.form["payment_mode"] or "Cash"

            # 🔒 Validation
            if not title or amount <= 0:
                flash("Invalid data entered!", "error")
                return redirect(url_for("add_expense"))

            db.add_expense(
                title=title,
                amount=amount,
                category_id=category_id,
                expense_date=date_val,
                payment_mode=payment
            )

            flash("Expense added successfully!", "success")
            return redirect(url_for("expenses"))

        except Exception as e:
            print("ADD ERROR:", e)
            flash("Something went wrong!", "error")
            return redirect(url_for("add_expense"))

    return render_template("add_expense.html", categories=categories)


# ───────────────── Edit Expense ─────────────────
@app.route("/edit-expenses/<int:id>", methods=["GET", "POST"])
def edit_expense(id):
    expense = db.get_expense_by_id(id)
    categories = db.get_all_categories()

    if not expense:
        flash("Expense not found!", "error")
        return redirect(url_for("expenses"))

    if request.method == "POST":
        try:
            # ✅ FIX DATE
            date_val = request.form["date"]
            if date_val:
                date_val = datetime.strptime(date_val, "%Y-%m-%d").date()
            else:
                date_val = date.today()

            db.update_expense(
                expense_id=id,
                title=request.form["title"],
                amount=float(request.form["amount"]),
                category_id=int(request.form["category_id"]),
                expense_date=date_val,
                description=request.form.get("description", ""),
                payment_mode=request.form["payment_mode"] or "Cash"
            )

            flash("Expense updated successfully!", "success")
            return redirect(url_for("expenses"))

        except Exception as e:
            print("EDIT ERROR:", e)
            flash("Error updating expense", "error")

    return render_template("edit_expenses.html", expense=expense, categories=categories)


# ───────────────── Delete Expense ─────────────────
@app.route("/delete-expense/<int:id>")
def delete_expense(id):
    db.delete_expense(id)
    flash("Expense deleted!", "success")
    return redirect(url_for("expenses"))


# ───────────────── Income ─────────────────
@app.route("/add-income", methods=["GET", "POST"])
def add_income():
    if request.method == "POST":
        try:
            source = request.form["source"].strip()
            amount = float(request.form["amount"])

            # ✅ FIX DATE
            date_val = request.form["date"]
            if date_val:
                date_val = datetime.strptime(date_val, "%Y-%m-%d").date()
            else:
                date_val = date.today()

            if not source or amount <= 0:
                flash("Invalid income data!", "error")
                return redirect(url_for("add_income"))

            db.add_income(source, amount, date_val)

            flash("Income added successfully!", "success")
            return redirect(url_for("dashboard"))

        except Exception as e:
            print("INCOME ERROR:", e)
            flash("Error adding income", "error")

    return render_template("add_income.html")


if __name__ == "__main__":
    app.run(debug=True)