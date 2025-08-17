import mysql.connector
from datetime import datetime, timedelta

# ✅ Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",        # change if needed
    password="yourpassword",  # change if needed
    database="LibraryDB"
)

cursor = db.cursor()

# -------------------------------
# FUNCTIONS
# -------------------------------

def add_book():
    title = input("Enter book title: ")
    author = input("Enter author: ")
    publisher = input("Enter publisher: ")
    year = int(input("Enter year: "))
    category = input("Enter category: ")
    copies = int(input("Enter total copies: "))

    cursor.execute("""
        INSERT INTO Books (title, author, publisher, year, category, total_copies, available_copies)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (title, author, publisher, year, category, copies, copies))
    db.commit()
    print("✅ Book added successfully!")


def add_member():
    name = input("Enter member name: ")
    email = input("Enter email: ")
    phone = input("Enter phone: ")

    cursor.execute("""
        INSERT INTO Members (name, email, phone)
        VALUES (%s, %s, %s)
    """, (name, email, phone))
    db.commit()
    print("✅ Member added successfully!")


def issue_book():
    book_id = int(input("Enter book ID: "))
    member_id = int(input("Enter member ID: "))

    # Check availability
    cursor.execute("SELECT available_copies FROM Books WHERE book_id = %s", (book_id,))
    result = cursor.fetchone()
    if not result or result[0] <= 0:
        print("❌ Book not available!")
        return

    # Reduce available copies
    cursor.execute("UPDATE Books SET available_copies = available_copies - 1 WHERE book_id = %s", (book_id,))

    # Insert into Transactions
    issue_date = datetime.today().date()
    due_date = issue_date + timedelta(days=14)
    cursor.execute("""
        INSERT INTO Transactions (book_id, member_id, issue_date, due_date)
        VALUES (%s, %s, %s, %s)
    """, (book_id, member_id, issue_date, due_date))

    db.commit()
    print("✅ Book issued successfully!")


def return_book():
    transaction_id = int(input("Enter transaction ID: "))

    # Fetch due date & book_id
    cursor.execute("SELECT book_id, due_date FROM Transactions WHERE transaction_id = %s AND return_date IS NULL", (transaction_id,))
    result = cursor.fetchone()
    if not result:
        print("❌ Invalid or already returned!")
        return

    book_id, due_date = result
    return_date = datetime.today().date()

    # Fine calculation (₹10 per day late)
    fine = 0
    if return_date > due_date:
        fine = (return_date - due_date).days * 10

    # Update transaction
    cursor.execute("""
        UPDATE Transactions 
        SET return_date = %s, fine = %s
        WHERE transaction_id = %s
    """, (return_date, fine, transaction_id))

    # Increase available copies
    cursor.execute("UPDATE Books SET available_copies = available_copies + 1 WHERE book_id = %s", (book_id,))
    db.commit()
    print(f"✅ Book returned! Fine: ₹{fine}")


def show_available_books():
    cursor.execute("SELECT book_id, title, author, available_copies FROM Books WHERE available_copies > 0")
    for row in cursor.fetchall():
        print(row)


def show_overdue_books():
    cursor.execute("""
        SELECT m.name, b.title, t.due_date
        FROM Transactions t
        JOIN Members m ON t.member_id = m.member_id
        JOIN Books b ON t.book_id = b.book_id
        WHERE t.return_date IS NULL AND CURDATE() > t.due_date
    """)
    for row in cursor.fetchall():
        print(row)


# -------------------------------
# MENU
# -------------------------------
def menu():
    while True:
        print("\n===== 📚 Library Management System =====")
        print("1. Add Book")
        print("2. Add Member")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Show Available Books")
        print("6. Show Overdue Books")
        print("7. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            add_member()
        elif choice == "3":
            issue_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            show_available_books()
        elif choice == "6":
            show_overdue_books()
        elif choice == "7":
            break
        else:
            print("❌ Invalid choice!")

# Run the system
menu()
