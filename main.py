from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database Setup
def init_db():
    conn = sqlite3.connect("fantasy_cricket.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS contests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        entry_fee INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        balance INTEGER DEFAULT 1000)''')
    conn.commit()
    conn.close()

init_db()

# Home Route
@app.route('/')
def home():
    return "Welcome to Fantasy Cricket App!"

# Create Contest
@app.route('/create_contest', methods=['POST'])
def create_contest():
    data = request.get_json()
    contest_name = data.get("name")
    entry_fee = data.get("entry_fee")
    
    conn = sqlite3.connect("fantasy_cricket.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contests (name, entry_fee) VALUES (?, ?)", (contest_name, entry_fee))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Contest Created Successfully"})

# Join Contest
@app.route('/join_contest', methods=['POST'])
def join_contest():
    data = request.get_json()
    username = data.get("username")
    contest_id = data.get("contest_id")

    conn = sqlite3.connect("fantasy_cricket.db")
    cursor = conn.cursor()

    cursor.execute("SELECT entry_fee FROM contests WHERE id = ?", (contest_id,))
    contest = cursor.fetchone()

    cursor.execute("SELECT balance FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not contest or not user:
        return jsonify({"error": "Invalid contest or user"}), 400

    entry_fee = contest[0]
    balance = user[0]

    if balance < entry_fee:
        return jsonify({"error": "Insufficient balance"}), 400

    cursor.execute("UPDATE users SET balance = balance - ? WHERE username = ?", (entry_fee, username))
    conn.commit()
    conn.close()

    return jsonify({"message": "Joined Contest Successfully"})

# Get Contest Details
@app.route('/contest_details', methods=['GET'])
def contest_details():
    conn = sqlite3.connect("fantasy_cricket.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contests")
    contests = cursor.fetchall()
    conn.close()

    return jsonify({"message": "Contest Details", "data": contests})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)