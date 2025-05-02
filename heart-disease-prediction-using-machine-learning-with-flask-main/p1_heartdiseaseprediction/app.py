import os
import joblib
import secrets
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
from sqlite3 import connect, Error
from sklearn.preprocessing import StandardScaler  # Add this for scaling

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(16))

# Email configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = os.getenv("EMAIL_USERNAME", "dhineshsubbarayan@gmail.com")
app.config["MAIL_PASSWORD"] = os.getenv("EMAIL_PASSWORD", "your app password")  # Use App Password
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

mail = Mail(app)

# Load the trained model and scaler
model_path = os.path.join("data", "models", "heart_disease_model.joblib")
scaler_path = os.path.join("data", "models", "scaler.joblib")
model = None
scaler = None

if os.path.exists(model_path):
    try:
        model = joblib.load(model_path)
        print(f"Model loaded successfully from {model_path}")
    except Exception as e:
        print(f"Error loading model: {e}")
else:
    print(f"Model file not found at {model_path}")

if os.path.exists(scaler_path):
    try:
        scaler = joblib.load(scaler_path)
        print(f"Scaler loaded successfully from {scaler_path}")
    except Exception as e:
        print(f"Error loading scaler: {e}")
else:
    print(f"Scaler file not found at {scaler_path}")

# Database connection function
def db_connection():
    try:
        con = connect("monicaheart.db")
        return con
    except Error as e:
        print(f"Database connection error: {e}")
        return None

# Home route
@app.route("/")
def home():
    if "username" in session:
        return render_template("home.html", name=session["username"])
    return redirect(url_for("signup"))

# Prediction form route
@app.route("/find")
def find():
    if "username" in session:
        return render_template("find.html", name=session["username"])
    return redirect(url_for("home"))

# Handle prediction request
@app.route("/check", methods=["POST"])
def check():
    if "username" not in session:
        return redirect(url_for("home"))

    if model is None:
        return render_template("find.html", msg="Model not loaded. Contact administrator.", name=session["username"])

    try:
        # Fetch input values from the form
        age = float(request.form["age"])
        chest_pain_type = int(request.form["r1"])
        bp = float(request.form["BP"])
        cholesterol = float(request.form["CH"])
        max_hr = float(request.form["maxhr"])
        st_depression = float(request.form["STD"])
        vessels_fluro = int(request.form["fluro"])
        thallium = int(request.form["Th"])

        # Prepare input data for prediction
        input_data = [[age, chest_pain_type, bp, cholesterol, max_hr, st_depression, vessels_fluro, thallium]]
        print("Input Data (Before Scaling):", input_data)  # Debugging: Print input data

        # Scale the input data using the saved scaler
        if scaler:
            input_data = scaler.transform(input_data)
            print("Input Data (After Scaling):", input_data)  # Debugging: Print scaled input data

        # Make prediction
        prediction = model.predict(input_data)
        print("Prediction:", prediction)  # Debugging: Print prediction

        # Return prediction result
        result = "Presence (Heart Disease Detected)" if prediction[0] == 1 else "Absence (No Heart Disease)"
        return render_template("find.html", msg=result, name=session["username"])
    except Exception as e:
        return render_template("find.html", msg=f"Error: {e}", name=session["username"])

# Signup route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["em"]
        username = request.form["un"]
        password = ''.join(secrets.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(8))  # Strong random password

        # Send email with password
        msg = Message(
            "Welcome to HeartDiseasePrediction",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email],
        )
        msg.body = f"Greetings from HeartDiseasePredictor! Your password is {password}"

        try:
            mail.send(msg)
            # Save user credentials to the database
            con = db_connection()
            if con:
                cursor = con.cursor()
                cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
                con.commit()
                con.close()
            return render_template("login.html", msg="Password has been mailed to you")
        except Exception as e:
            return render_template("signup.html", msg=f"Error: {e}")
    return render_template("signup.html")

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["un"]
        password = request.form["pw"]

        try:
            # Verify user credentials
            con = db_connection()
            if con:
                cursor = con.cursor()
                cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
                data = cursor.fetchone()
                con.close()

                if data:
                    session["username"] = username
                    session.permanent = True
                    return redirect(url_for("home"))
                return render_template("login.html", msg="Invalid login")
        except Exception as e:
            return render_template("login.html", msg=f"Error: {e}")
    return render_template("login.html")

# Forgot password route
@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        username = request.form["un"]
        email = request.form["em"]
        new_password = ''.join(secrets.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(8))  # Strong random password

        # Send email with new password
        msg = Message(
            "Password Reset - HeartDiseasePrediction",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email],
        )
        msg.body = f"Your new password is {new_password}"

        try:
            mail.send(msg)
            # Update password in the database
            con = db_connection()
            if con:
                cursor = con.cursor()
                cursor.execute("UPDATE user SET password = ? WHERE username = ?", (new_password, username))
                con.commit()
                con.close()
            return render_template("login.html", msg="Password has been mailed to you")
        except Exception as e:
            return render_template("forgot.html", msg=f"Error: {e}")
    return render_template("forgot.html")

# Logout route
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)