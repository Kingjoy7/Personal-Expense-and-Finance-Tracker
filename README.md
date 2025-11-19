# Personal Expense and Savings Tracker

## Prerequisites
- Python 3.8+
- MySQL 8.x
- pip install -r requirements.txt (Flask, mysql-connector-python)

## Setup DB
1. Create DB and schema:
   mysql -u root -p < setup.sql

## Run app
1. Set DB credentials in app.py DB_CONFIG if different.
2. Install requirements:
   pip install Flask mysql-connector-python
3. Run:
   python app.py
4. Open browser at http://localhost:5000

## Notes
- Use the UI to add transactions, observe triggers and cascade deletion.
- To view triggers/procedures use MySQL Workbench or run SHOW TRIGGERS; SHOW PROCEDURE STATUS WHERE db='expense_tracker';
