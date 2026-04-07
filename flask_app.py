from flask import Flask, render_template, request, redirect, url_for
import db_operations as db

app = Flask(__name__)

@app.route("/")
def dashboard():
    summary = db.get_dashboard_summary(1)
    return render_template("dashboard.html", summary=summary)

@app.template_filter('format_inr')
def format_inr(value):
    return f"₹{value:,.2f}"

@app.route("/expenses")
def expenses():
    data = db.get_expenses(1)
    return render_template("expenses.html", expenses=data)

@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        db.add_expense(
            title=request.form["title"],
            amount=float(request.form["amount"]),
            category_id=int(request.form["category_id"]),
            expense_date=request.form["date"],
            payment_mode=request.form["payment_mode"]
        )
        return redirect(url_for("dashboard"))

    categories = db.get_all_categories()
    return render_template("add_expense.html", categories=categories)

if __name__ == "__main__":
    app.run(debug=True)