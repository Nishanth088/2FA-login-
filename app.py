from flask import Flask, render_template, request, redirect, url_for, session, flash
import random, json, os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Load users from file (line by line)
def load_users():
    users = {}
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            for line in f:
                if line.strip():
                    record = json.loads(line.strip())
                    users[record["email"]] = {"password": record["password"]}
    return users

# Save users to file (line by line)
def save_users(users):
    with open("users.json", "w") as f:
        for email, data in users.items():
            record = {"email": email, "password": data["password"]}
            f.write(json.dumps(record) + "\n")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        users = load_users()
        if email in users:
            flash("⚠️ Email already registered!", "error")
            return redirect(url_for("register"))

        users[email] = {"password": password}
        save_users(users)

        flash("✅ Registered successfully! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        users = load_users()
        if email not in users or users[email]["password"] != password:
            flash("❌ Invalid credentials!", "error")
            return redirect(url_for("login"))

        otp = str(random.randint(100000, 999999))
        session["otp"] = otp
        session["email"] = email

        print(f"OTP for {email} is: {otp}")  # Debug: shows in terminal
        flash("🔑 OTP has been generated! (Check terminal)", "info")
        return redirect(url_for("verify"))

    return render_template("login.html")

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

@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        flash("⚠️ Please login first!", "error")
        return redirect(url_for("login"))
    return render_template("dashboard.html", email=session["email"])

@app.route("/logout")
def logout():
    session.clear()
    flash("✅ Logged out successfully.", "success")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
