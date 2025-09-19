from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import mysql.connector

# -----------------------
# Flask App Setup
# -----------------------
app = Flask(__name__)
app.secret_key = "supersecretkey"

# -----------------------
# MySQL Connection
# -----------------------
mydb = mysql.connector.connect(
    host="localhost",
    user="root",       # XAMPP default user
    password="",       # XAMPP default password
    database="flaskdb",# database created in phpMyAdmin
    port=3306          # change if your MySQL uses a different port
)
cursor = mydb.cursor(dictionary=True)

# -----------------------
# Routes
# -----------------------
@app.route("/")
def home():
    return render_template("index.html")

# Register Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        if user:
            flash("⚠️ Email already registered!", "error")
            return redirect(url_for("register"))

        # Insert new user
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        mydb.commit()

        flash("✅ Registered successfully! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Fetch user from database
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        if not user or user["password"] != password:
            flash("❌ Invalid credentials!", "error")
            return redirect(url_for("login"))

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        session["otp"] = otp
        session["email"] = email

        print(f"OTP for {email} is: {otp}")  # Debug: shows in terminal
        flash("🔑 OTP has been generated! (Check terminal)", "info")
        return redirect(url_for("verify"))

    return render_template("login.html")

# OTP Verification Route
@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        otp_entered = request.form["otp"]
        if otp_entered == session.get("otp"):
            flash("✅ Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("❌ Invalid OTP!", "error")
            return redirect(url_for("verify"))

    return render_template("verify.html")

# Dashboard Route
@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        flash("⚠️ Please login first!", "error")
        return redirect(url_for("login"))
    return render_template("dashboard.html", email=session["email"])

# Logout Route
@app.route("/logout")
def logout():
    session.clear()
    flash("✅ Logged out successfully.", "success")
    return redirect(url_for("login"))

# -----------------------
# Run App
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
