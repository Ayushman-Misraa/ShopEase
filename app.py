from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlite3
from utils.auth import login_required, admin_required

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change before production

# ------- Database Connection -------
def get_db():
    conn = sqlite3.connect("instance/shop.db")
    conn.row_factory = sqlite3.Row
    return conn


# ------------------- ROUTES ---------------------

@app.route("/")
def home():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        db = get_db()
        data = db.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (user, pwd)
        ).fetchone()

        if data:
            session["user"] = user
            session["role"] = data["role"]   # "admin" or "staff"
            return redirect("/dashboard")
        else:
            flash("Invalid username or password")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# ------------------- BILLING ---------------------

@app.route("/billing")
@login_required
def billing():
    return render_template("billing.html")


# ------------------- PRODUCTS ---------------------

@app.route("/products")
@admin_required
def products():
    db = get_db()
    all_products = db.execute("SELECT * FROM products").fetchall()
    return render_template("products.html", products=all_products)


# -----------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
