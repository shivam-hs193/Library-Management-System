from flask import Flask, request, jsonify, render_template
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)

# -------------------------------
# DATABASE CONNECTION
# -------------------------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",            # change if needed
        password="Shivam@nn2003",
        database="LibraryDB"
    )

# -------------------------------
# ADD BOOK
# -------------------------------
@app.route("/add-book", methods=["POST"])
def add_book():
    data = request.json
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO Books (title, author, publisher, year, category, total_copies, available_copies)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        data["title"],
        data["author"],
        data["publisher"],
        data["year"],
        data["category"],
        data["copies"],
        data["copies"]
    ))

    db.commit()
    return jsonify({"message": "Book added successfully"})

# -------------------------------
# ADD MEMBER
# -------------------------------
@app.route("/add-member", methods=["POST"])
def add_member():
    data = request.json
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO Members (name, email, phone)
        VALUES (%s,%s,%s)
    """, (
        data["name"],
        data["email"],
        data["phone"]
    ))

    db.commit()
    return jsonify({"message": "Member added successfully"})

# -------------------------------
# ISSUE BOOK
# -------------------------------
@app.route("/issue-book", methods=["POST"])
def issue_book():
    data = request.json
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT available_copies FROM Books WHERE book_id=%s", (data["book_id"],))
    result = cursor.fetchone()

    if not result or result[0] <= 0:
        return jsonify({"error": "Book not available"}), 400

    cursor.execute(
        "UPDATE Books SET available_copies = available_copies - 1 WHERE book_id=%s",
        (data["book_id"],)
    )

    issue_date = datetime.today().date()
    due_date = issue_date + timedelta(days=14)

    cursor.execute("""
        INSERT INTO Transactions (book_id, member_id, issue_date, due_date)
        VALUES (%s,%s,%s,%s)
    """, (
        data["book_id"],
        data["member_id"],
        issue_date,
        due_date
    ))

    db.commit()
    return jsonify({"message": "Book issued successfully", "due_date": str(due_date)})

# -------------------------------
# RETURN BOOK
# -------------------------------
@app.route("/return-book", methods=["POST"])
def return_book():
    data = request.json
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT book_id, due_date
        FROM Transactions
        WHERE transaction_id=%s AND return_date IS NULL
    """, (data["transaction_id"],))

    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "Invalid or already returned"}), 400

    book_id, due_date = result
    return_date = datetime.today().date()

    fine = 0
    if return_date > due_date:
        fine = (return_date - due_date).days * 10

    cursor.execute("""
        UPDATE Transactions
        SET return_date=%s, fine=%s
        WHERE transaction_id=%s
    """, (
        return_date,
        fine,
        data["transaction_id"]
    ))

    cursor.execute(
        "UPDATE Books SET available_copies = available_copies + 1 WHERE book_id=%s",
        (book_id,)
    )

    db.commit()
    return jsonify({"message": "Book returned", "fine": fine})

# -------------------------------
# SHOW AVAILABLE BOOKS
# -------------------------------
@app.route("/available-books", methods=["GET"])
def show_available_books():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT book_id, title, author, available_copies
        FROM Books
        WHERE available_copies > 0
    """)

    return jsonify(cursor.fetchall())

# -------------------------------
# SHOW OVERDUE BOOKS
# -------------------------------
@app.route("/overdue-books", methods=["GET"])
def show_overdue_books():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT m.name, b.title, t.due_date
        FROM Transactions t
        JOIN Members m ON t.member_id = m.member_id
        JOIN Books b ON t.book_id = b.book_id
        WHERE t.return_date IS NULL AND CURDATE() > t.due_date
    """)

    return jsonify(cursor.fetchall())

@app.route("/")
def index():
    return render_template("index.html")

# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
