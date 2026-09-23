import sqlite3
from datetime import datetime

PREDICTIONS_DB = "predictions.db"
BOOKINGS_DB = "bookings.db"


# =========================================
# CONNECTIONS
# =========================================

def get_predictions_db():
    conn = sqlite3.connect(PREDICTIONS_DB)
    conn.row_factory = sqlite3.Row
    return conn


def get_bookings_db():
    conn = sqlite3.connect(BOOKINGS_DB)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================
# INITIALIZATION (tables create karega agar exist nahi karte)
# =========================================

def init_predictions_db():
    conn = get_predictions_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            age INTEGER,
            sex TEXT,
            chest_pain TEXT,
            resting_bp INTEGER,
            cholesterol INTEGER,
            fasting_bs INTEGER,
            resting_ecg TEXT,
            max_hr INTEGER,
            exercise_angina TEXT,
            oldpeak REAL,
            st_slope TEXT,
            result TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def init_bookings_db():
    conn = get_bookings_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            phone TEXT,
            email TEXT,
            doctor TEXT,
            appointment_date TEXT,
            appointment_time TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def init_dbs():
    init_predictions_db()
    init_bookings_db()


# =========================================
# INSERTS
# =========================================

def save_prediction(data):
    conn = get_predictions_db()
    conn.execute("""
        INSERT INTO predictions (
            patient_name, age, sex, chest_pain, resting_bp, cholesterol,
            fasting_bs, resting_ecg, max_hr, exercise_angina, oldpeak,
            st_slope, result, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["patient_name"], data["age"], data["sex"], data["chest_pain"],
        data["resting_bp"], data["cholesterol"], data["fasting_bs"],
        data["resting_ecg"], data["max_hr"], data["exercise_angina"],
        data["oldpeak"], data["st_slope"], data["result"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()


def save_booking(data):
    conn = get_bookings_db()
    conn.execute("""
        INSERT INTO bookings (
            patient_name, phone, email, doctor, appointment_date,
            appointment_time, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["patient_name"], data["phone"], data["email"], data["doctor"],
        data["appointment_date"], data["appointment_time"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()


# =========================================
# READS (admin panel ke liye)
# =========================================

def get_all_predictions():
    conn = get_predictions_db()
    rows = conn.execute("SELECT * FROM predictions ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def get_all_bookings():
    conn = get_bookings_db()
    rows = conn.execute("SELECT * FROM bookings ORDER BY id DESC").fetchall()
    conn.close()
    return rows