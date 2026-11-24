
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from pathlib import Path
from datetime import date

app = Flask(__name__)

DB_PATH = Path(
    os.environ.get("DB_PATH", Path(__file__).parent / "mymoney.db")
)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount INTEGER NOT NULL,
                category TEXT NOT NULL,
                kind TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)


@app.route("/")
def index():
    today = date.today()

    months = []
    for i in range(6, -1, -1):
        year = today.year
        month = today.month - i

        while month <= 0:
            month += 12
            year -= 1

        months.append(f"{year:04d}-{month:02d}")

    with get_db() as conn:
        transactions = conn.execute(
            "SELECT * FROM transactions ORDER BY date DESC, id DESC"
        ).fetchall()

        income = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE kind='income'"
        ).fetchone()[0]

        expense = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE kind='expense'"
        ).fetchone()[0]

        placeholders = ",".join("?" for _ in months)

        monthly_rows = conn.execute(f"""
            SELECT
                substr(date, 1, 7) AS month,
                SUM(CASE WHEN kind='income' THEN amount ELSE 0 END) AS income,
                SUM(CASE WHEN kind='expense' THEN amount ELSE 0 END) AS expense
            FROM transactions
            WHERE substr(date, 1, 7) IN ({placeholders})
            GROUP BY substr(date, 1, 7)
        """, months).fetchall()

    monthly_data = {
        row["month"]: {
            "income": row["income"],
            "expense": row["expense"]
        }
        for row in monthly_rows
    }

    chart_labels = [f"{int(month[5:7])}월" for month in months]

    chart_income = [
        monthly_data.get(month, {}).get("income", 0)
        for month in months
    ]

    chart_expense = [
        monthly_data.get(month, {}).get("expense", 0)
        for month in months
    ]

    return render_template(
        "index.html",
        transactions=transactions,
        income=income,
        expense=expense,
        balance=income - expense,
        chart_labels=chart_labels,
        chart_income=chart_income,
        chart_expense=chart_expense
    )


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "").strip()
    kind = request.form.get("kind", "")
    transaction_date = request.form.get("date", "")

    try:
        amount = int(request.form.get("amount", "0"))
    except ValueError:
        return "금액을 숫자로 입력해 주세요.", 400

    if (
        not title or not category or amount <= 0
        or kind not in ("income", "expense")
        or not transaction_date
    ):
        return "입력 내용을 확인해 주세요.", 400

    with get_db() as conn:
        conn.execute(
            """INSERT INTO transactions
            (title, amount, category, kind, date)
            VALUES (?, ?, ?, ?, ?)""",
            (title, amount, category, kind, transaction_date)
        )

    return redirect(url_for("index"))


@app.route("/delete/<int:transaction_id>", methods=["POST"])
def delete(transaction_id):
    with get_db() as conn:
        conn.execute(
            "DELETE FROM transactions WHERE id = ?",
            (transaction_id,)
        )

    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
