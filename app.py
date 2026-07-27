from flask import Flask, jsonify, request, send_from_directory
import sqlite3
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
DB_FILE = BASE_DIR / "database.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT,
            ats_score INTEGER,
            coding_score INTEGER,
            status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT,
            package TEXT,
            hiring_status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            company_id INTEGER,
            applied_on TEXT,
            current_status TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(company_id) REFERENCES companies(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            company_id INTEGER,
            interview_date TEXT,
            interview_status TEXT,
            feedback TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(company_id) REFERENCES companies(id)
        )
    """)

    conn.commit()
    conn.close()

def add_sample_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    if total_students > 0:
        conn.close()
        return

    students = [
        ("Rahul Verma", "CSE", "rahul@ggits.edu", 84, 76, "Interview"),
        ("Priya Sharma", "IT", "priya@ggits.edu", 88, 82, "Shortlisted"),
        ("Aman Patel", "ECE", "aman@ggits.edu", 76, 70, "Coding Test"),
        ("Sneha Gupta", "CSE", "sneha@ggits.edu", 91, 86, "Placed"),
        ("Aditya Sahu", "ME", "aditya@ggits.edu", 69, 62, "Applied"),
        ("Neha Jain", "CSE", "neha@ggits.edu", 80, 74, "Applied")
    ]

    companies = [
        ("Infosys", "System Engineer", "3.6 LPA", "Hiring Open"),
        ("TCS", "Ninja Developer", "3.4 LPA", "Hiring Open"),
        ("Wipro", "Project Engineer", "3.5 LPA", "Hiring Open"),
        ("Accenture", "Associate Software Engineer", "4.5 LPA", "Registration Soon"),
        ("Capgemini", "Analyst", "4.0 LPA", "Hiring Open"),
        ("Cognizant", "Programmer Analyst", "4.2 LPA", "Closed")
    ]

    cursor.executemany(
        "INSERT INTO students (name, department, email, ats_score, coding_score, status) VALUES (?, ?, ?, ?, ?, ?)",
        students
    )
    cursor.executemany(
        "INSERT INTO companies (name, role, package, hiring_status) VALUES (?, ?, ?, ?)",
        companies
    )

    applications = [
        (1, 1, "2026-07-10", "Interview"),
        (1, 2, "2026-07-12", "Applied"),
        (2, 1, "2026-07-11", "Shortlisted"),
        (3, 3, "2026-07-14", "Coding Test"),
        (4, 5, "2026-07-16", "Selected")
    ]

    interviews = [
        (1, 1, "2026-08-05", "Scheduled", "Good resume and basic coding skills."),
        (2, 1, "2026-08-06", "Scheduled", "Strong communication."),
        (4, 5, "2026-08-02", "Completed", "Selected for final round.")
    ]

    cursor.executemany(
        "INSERT INTO applications (student_id, company_id, applied_on, current_status) VALUES (?, ?, ?, ?)",
        applications
    )
    cursor.executemany(
        "INSERT INTO interviews (student_id, company_id, interview_date, interview_status, feedback) VALUES (?, ?, ?, ?, ?)",
        interviews
    )

    conn.commit()
    conn.close()

def rows_to_list(rows):
    data = []
    for row in rows:
        data.append(dict(row))
    return data

@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/<path:file_name>")
def static_pages(file_name):
    allowed = [
        "index.html", "about.html", "students.html", "companies.html",
        "college.html", "login.html", "dashboard.html", "resume-score.html",
        "mock-interview.html", "coding-test.html", "hr-dashboard.html",
        "feedback.html", "style.css", "script.js"
    ]
    if file_name in allowed:
        return send_from_directory(BASE_DIR, file_name)
    return "File not found", 404

@app.route("/students")
def students_page():
    return send_from_directory(BASE_DIR, "students.html")

@app.route("/companies")
def companies_page():
    return send_from_directory(BASE_DIR, "companies.html")

@app.route("/college")
def college_page():
    return send_from_directory(BASE_DIR, "college.html")

@app.route("/resume")
def resume_page():
    return send_from_directory(BASE_DIR, "resume-score.html")

@app.route("/coding")
def coding_page():
    return send_from_directory(BASE_DIR, "coding-test.html")

@app.route("/mock")
def mock_page():
    return send_from_directory(BASE_DIR, "mock-interview.html")

@app.route("/dashboard")
def dashboard_page():
    return send_from_directory(BASE_DIR, "dashboard.html")

@app.route("/login")
def login_page():
    return send_from_directory(BASE_DIR, "login.html")

@app.route("/api/students")
def get_students():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))

@app.route("/api/companies")
def get_companies():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM companies ORDER BY name").fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))

@app.route("/api/applications")
def get_applications():
    conn = get_connection()
    rows = conn.execute("""
        SELECT applications.id, students.name AS student_name, companies.name AS company_name,
               applications.applied_on, applications.current_status
        FROM applications
        JOIN students ON students.id = applications.student_id
        JOIN companies ON companies.id = applications.company_id
        ORDER BY applications.id DESC
    """).fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))

@app.route("/api/contact", methods=["POST"])
def contact():
    form_data = request.get_json() or {}
    name = form_data.get("name", "Student")
    return jsonify({
        "message": f"Thanks {name}, your message was received by the demo portal."
    })

@app.route("/api/stats")
def stats():
    conn = get_connection()
    total_students = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    total_companies = conn.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
    total_applications = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
    conn.close()
    return jsonify({
        "students": total_students,
        "companies": total_companies,
        "applications": total_applications,
        "placed": 512
    })

if __name__ == "__main__":
    create_tables()
    add_sample_data()
    print("GGITS Placement Platform running at http://127.0.0.1:5000")
    app.run(debug=True)
