from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash, check_password_hash
from chatbot_ai import chatbot_response, add_pdf_text

app = Flask(__name__)
app.secret_key = "secret123"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="chatbot_db"
)
cursor = db.cursor(dictionary=True)

# ----- Login / Register -----
@app.route("/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if not user:
            hashed_password = generate_password_hash(password)
            cursor.execute("INSERT INTO users (username, password) VALUES (%s,%s)", (username, hashed_password))
            db.commit()
            user_id = cursor.lastrowid
        else:
            if not check_password_hash(user["password"], password):
                return "Invalid password!"
            user_id = user["id"]

        session["user_id"] = user_id
        session["username"] = username
        return redirect("/chat")
    return render_template("login.html")

# ----- Chat Page -----
@app.route("/chat")
def chat_page():
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]
    cursor.execute(
        "SELECT message, response FROM messages WHERE user_id=%s ORDER BY created_at ASC", (user_id,)
    )
    chats = cursor.fetchall()
    return render_template("chat.html", username=session["username"], chats=chats)

# ----- Chat API -----
@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.get_json()
    message = data["message"]
    user_id = session["user_id"]

    reply = chatbot_response(message)

    cursor.execute(
        "INSERT INTO messages (user_id, message, response) VALUES (%s,%s,%s)",
        (user_id, message, reply)
    )
    db.commit()

    return jsonify({"reply": reply})

# ----- PDF Upload -----
@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    if "user_id" not in session:
        return redirect("/")
    if 'pdf' not in request.files:
        return "No file selected!"
    file = request.files['pdf']
    if file.filename == '':
        return "No file selected!"
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    add_pdf_text(filepath)
    return redirect("/chat")

# ----- Logout -----
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
