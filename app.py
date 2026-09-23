from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import joblib
from functools import wraps

import db

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-key"  # session ke liye zaroori

model = joblib.load("Knn_model.pkl")
scaler = joblib.load("Scaler.pkl")
columns = joblib.load("features.pkl")

# App start hote hi dono databases/tables ban jayenge
db.init_dbs()

# Deploy se pehle yeh zaroor change karna
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "changeme123"


# =========================================
# ADMIN LOGIN REQUIRED DECORATOR
# =========================================

def admin_login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return wrapper


# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================
# ASSESSMENT
# =========================================

@app.route("/assessment", methods=["GET", "POST"])
def assessment():

    if request.method == "POST":

        patient_name = request.form.get("patient_name", "")
        age = int(request.form.get("age"))
        sex = request.form.get("sex")
        chest_pain = request.form.get("chest_pain")
        resting_bp = int(request.form.get("resting_bp"))
        cholesterol = int(request.form.get("cholesterol"))
        fasting_bs = int(request.form.get("fasting_bs"))
        resting_ecg = request.form.get("resting_ecg")
        max_hr = int(request.form.get("max_hr"))
        exercise_angina = request.form.get("exercise_angina")
        oldpeak = float(request.form.get("oldpeak"))
        st_slope = request.form.get("st_slope")

        raw_input = {
            'Age': age,
            'RestingBP': resting_bp,
            'Cholesterol': cholesterol,
            'FastingBS': fasting_bs,
            'MaxHR': max_hr,
            'Oldpeak': oldpeak,
            'Sex_' + sex: 1,
            'ChestPainType_' + chest_pain: 1,
            'RestingECG_' + resting_ecg: 1,
            'ExerciseAngina_' + exercise_angina: 1,
            'ST_Slope_' + st_slope: 1
        }

        input_df = pd.DataFrame([raw_input])

        for col in columns:
            if col not in input_df.columns:
                input_df[col] = 0

        input_df = input_df[columns]

        scaled_input = scaler.transform(input_df)
        prediction = model.predict(scaled_input)[0]

        result = "high" if prediction == 1 else "low"

        # Prediction ko database mein save karo
        db.save_prediction({
            "patient_name": patient_name,
            "age": age,
            "sex": sex,
            "chest_pain": chest_pain,
            "resting_bp": resting_bp,
            "cholesterol": cholesterol,
            "fasting_bs": fasting_bs,
            "resting_ecg": resting_ecg,
            "max_hr": max_hr,
            "exercise_angina": exercise_angina,
            "oldpeak": oldpeak,
            "st_slope": st_slope,
            "result": result
        })

        return render_template(
            "result.html",
            result=result,
            patient_name=patient_name
        )

    return render_template("assessment.html")


# =========================================
# DOCTORS CONSULTATION PAGE
# =========================================

@app.route("/consultation", methods=["GET", "POST"])
def consultation():

    booking_success = False

    if request.method == "POST":

        patient_name = request.form.get("patient_name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        doctor = request.form.get("doctor")
        appointment_date = request.form.get("appointment_date")
        appointment_time = request.form.get("appointment_time")

        # Booking ko database mein save karo
        db.save_booking({
            "patient_name": patient_name,
            "phone": phone,
            "email": email,
            "doctor": doctor,
            "appointment_date": appointment_date,
            "appointment_time": appointment_time
        })

        booking_success = True

    return render_template(
        "consultation.html",
        booking_success=booking_success
    )


# =========================================
# ADMIN PANEL
# =========================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "Rognidaan" and password == "Rognidaan@123":
            session["is_admin"] = True
            if len(password)>=8 :
                return redirect(url_for("admin_dashboard"))
        else:
            error = "Invalid username or password."

    return render_template("admin_login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin_login"))


@app.route("/admin")
@admin_login_required
def admin_dashboard():
    predictions = db.get_all_predictions()
    bookings = db.get_all_bookings()

    return render_template(
        "admin_dashboard.html",
        predictions=predictions,
        bookings=bookings
    )


# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":
    app.run(debug=True)