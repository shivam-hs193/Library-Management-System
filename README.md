# 📚 Library Management System (Flask + MySQL)

A **full-stack Library Management System** built using **Python (Flask)**, **MySQL**, and **HTML/CSS/JavaScript**.  
The entire application runs from a **single command** and is accessed through a web browser.

---

## 🚀 Features
- Add new books and members  
- Issue and return books  
- Automatic due date & fine calculation  
- View available books  
- View overdue books  
- Database integrity using foreign keys  
- Optimized queries using indexes  

---

## 🏗️ System Architecture
Browser (HTML / CSS / JavaScript)
↓
Flask Backend (APIs + Template Rendering)
↓
MySQL Database

---

## 📁 Project Structure
'''
Library-Management-System/
│
├── backend/
│   ├── app.py                  # Flask backend (main entry point)
│   ├── library_management.sql  # Database schema + sample data
│   │
│   ├── templates/
│   │   └── index.html          # Frontend UI
│   │
│   └── static/
│       ├── style.css           # Stylesheet
│       └── script.js           # Frontend logic
│   ├── mysql-connector.py      # CLI version (reference / optional)
│ 
└── README.md
'''

---

## 🛠️ Requirements
- **Python** 3.10 or higher  
- **MySQL Server** 8.0 or higher  
- **MySQL Workbench** (recommended)

### Python Dependencies
```bash
pip install flask mysql-connector-python
