Expense Tracker – DBMS Project
PES University — UE23CS351A (DBMS Course Project)

Team:

Sujoy Sen – PES2UG23CS621

Tahir Shafiq – PES2UG23CS639

📌 Project Overview

This project implements a database-driven Expense Tracker using Flask (Python) and MySQL.
It demonstrates key DBMS concepts including:

Stored Procedures

Triggers

SQL Functions

Joins, Nested Queries & Aggregates

ON DELETE CASCADE

Frontend interaction via Flask

The application allows users to:

Add transactions (income/expense) via a stored procedure

Automatically update financial goals via triggers

View all tables (Users, Categories, Transactions, Goals, Budgets)

Delete users and observe cascading delete effects

Display DB errors through Flask flash messages

This is a simple, academic mini-project designed to demonstrate DBMS features through a working web application.

🗂 Project Structure
/project
│── app.py               # Flask Application
│── project.sql          # MySQL Schema + Triggers + Procedure + Function + Sample Data
│── README.md            # Project Documentation

🛠 Technologies Used

Python 3.x

Flask

MySQL

mysql-connector-python

HTML/CSS (inline templates)

MySQL Workbench (optional)

⚙ How to Run the Project
1. Install dependencies
pip install flask mysql-connector-python

2. Import the SQL file

Run the following:

mysql -u root -p < project.sql

3. Start the Flask Application
python app.py

4. Open in Browser

Visit:

http://localhost:5000


Your Expense Tracker UI should now be visible.

🧩 Database Features Implemented
✅ Triggers

check_transaction_type_before_insert
Ensures transaction type matches the category type (income/expense).

check_transaction_type_before_update
Prevents invalid updates to the transaction-category mapping.

apply_income_to_goal_after_insert
Automatically updates the nearest goal when income is added.

✅ Stored Procedure
sp_add_transaction

Used by Flask to insert transactions safely and consistently.

✅ SQL Function
fn_get_user_balance

Returns total income − total expense for a user.

✅ Cascade Delete

Deleting a user removes:

Their transactions

Their budgets

Their goals

This demonstrates ON DELETE CASCADE in action.

🔍 Sample Queries Included

Nested Query – users with expenses > X

Join Query – transactions with category & user names

Aggregate Query – monthly totals & top expense categories

All included inside project.sql.

🌐 Frontend Features (Flask UI)

Add Transaction form (calls stored procedure)

View:

Transactions

Goals

Budgets

Users

Delete user (CASCADE effect)

Flash message support (success/error)

Table toggling using checkboxes

📸 Screenshots to Include (for report)

Home page (default)

Viewing goals & budgets

Add transaction (before submit)

Add transaction success flash message

Transactions table showing new row

Goals before income

Goals after income (trigger effect)

Users before delete

Delete user action

Cascade delete result

🧪 Code Snippets (Procedure/Trigger Invocation)
Call Stored Procedure:
cur.callproc('sp_add_transaction', (user_id, category_id, amount, typ, date))

Call Function:
cur.execute("SELECT fn_get_user_balance(%s)", (user_id,))

Triggers:

Automatically fire when inserting or updating a transaction.

📘 Conclusion

This Expense Tracker project successfully demonstrates how a Python web app interacts with a relational database while enforcing rules and automation using:

Triggers

Procedures

Functions

Constraints

Cascading actions

It is a simple, effective example of integrating DBMS concepts into a real application.