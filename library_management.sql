-- ================================
-- Library Management System (LMS)
-- ================================

-- 1️⃣ Create Database
CREATE DATABASE IF NOT EXISTS LibraryDB;
USE LibraryDB;

-- 2️⃣ Create Tables

-- Books Table
CREATE TABLE Books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    publisher VARCHAR(255),
    year INT,
    category VARCHAR(100),
    total_copies INT DEFAULT 1,
    available_copies INT DEFAULT 1
);

-- Members Table
CREATE TABLE Members (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    membership_date DATE DEFAULT (CURRENT_DATE)
);

-- Transactions Table (Book Issue/Return)
CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    book_id INT,
    member_id INT,
    issue_date DATE DEFAULT (CURRENT_DATE),
    due_date DATE,
    return_date DATE,
    fine DECIMAL(10,2) DEFAULT 0,
    FOREIGN KEY (book_id) REFERENCES Books(book_id),
    FOREIGN KEY (member_id) REFERENCES Members(member_id)
);

-- 3️⃣ Insert Sample Data

-- Books
INSERT INTO Books (title, author, publisher, year, category, total_copies, available_copies) VALUES
('The Alchemist', 'Paulo Coelho', 'HarperCollins', 1988, 'Fiction', 5, 5),
('Introduction to Algorithms', 'Thomas H. Cormen', 'MIT Press', 2009, 'Education', 3, 3),
('Harry Potter and the Philosopher''s Stone', 'J.K. Rowling', 'Bloomsbury', 1997, 'Fantasy', 4, 4),
('Clean Code', 'Robert C. Martin', 'Prentice Hall', 2008, 'Programming', 2, 2);

-- Members
INSERT INTO Members (name, email, phone) VALUES
('Alice Johnson', 'alice@example.com', '9876543210'),
('Bob Smith', 'bob@example.com', '9876543211'),
('Charlie Brown', 'charlie@example.com', '9876543212');

-- 4️⃣ Example Queries

-- (A) Show all available books
SELECT title, author, available_copies
FROM Books
WHERE available_copies > 0;

-- (B) Issue a Book (reduce available copies & create transaction)
UPDATE Books
SET available_copies = available_copies - 1
WHERE book_id = 1 AND available_copies > 0;

INSERT INTO Transactions (book_id, member_id, issue_date, due_date)
VALUES (1, 1, CURRENT_DATE, DATE_ADD(CURRENT_DATE, INTERVAL 14 DAY));

-- (C) Return a Book (update return_date, fine, increase available copies)
UPDATE Transactions
SET return_date = CURRENT_DATE,
    fine = CASE
        WHEN CURRENT_DATE > due_date
        THEN DATEDIFF(CURRENT_DATE, due_date) * 10
        ELSE 0
    END
WHERE transaction_id = 1;

UPDATE Books
SET available_copies = available_copies + 1
WHERE book_id = 1;

-- (D) Check Overdue Books
SELECT m.name, b.title, t.due_date, 
       DATEDIFF(CURRENT_DATE, t.due_date) AS days_overdue
FROM Transactions t
JOIN Members m ON t.member_id = m.member_id
JOIN Books b ON t.book_id = b.book_id
WHERE t.return_date IS NULL AND CURRENT_DATE > t.due_date;

-- (E) Most Borrowed Books Report
SELECT b.title, COUNT(t.transaction_id) AS times_borrowed
FROM Transactions t
JOIN Books b ON t.book_id = b.book_id
GROUP BY b.title
ORDER BY times_borrowed DESC;

-- (F) Active Members (who borrowed most)
SELECT m.name, COUNT(t.transaction_id) AS books_borrowed
FROM Transactions t
JOIN Members m ON t.member_id = m.member_id
GROUP BY m.name
ORDER BY books_borrowed DESC;
