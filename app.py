from flask import Flask, render_template_string, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "dev_secret_key"

# --- Configure DB connection ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'tahir@398',
    'database': 'expense_tracker',
    'raise_on_warnings': True
}

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

# --- Enhanced Template ---
BASE_HTML = """
<!doctype html>
<html>
<head>
  <title>Expense Tracker DB Demo</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 1000px; margin: 20px auto; padding: 0 20px; }
    table { border-collapse: collapse; width: 100%; margin-bottom: 16px; }
    th,td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background: #4CAF50; color: white; }
    form { margin-bottom: 16px; padding: 12px; border: 1px solid #eee; background: #fafafa; border-radius: 4px; }
    .row { display:flex; gap:8px; flex-wrap:wrap; align-items:center; margin-bottom: 8px; }
    .col { flex: 1 1 180px; }
    input, select { width: 100%; padding: 6px; box-sizing: border-box; }
    .btn { padding:8px 16px; border:1px solid #4CAF50; background:#4CAF50; color:white; cursor:pointer; border-radius:4px; }
    .btn:hover { background:#45a049; }
    .btn-danger { background:#f44336; border-color:#f44336; }
    .btn-danger:hover { background:#da190b; }
    .notice { padding:10px; background:#e7f3fe; border-left:4px solid #2196F3; margin-bottom:16px; }
    .error { padding:10px; background:#ffebee; border-left:4px solid #f44336; margin-bottom:16px; }
    .success { padding:10px; background:#e8f5e9; border-left:4px solid #4CAF50; margin-bottom:16px; }
    h2 { color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 8px; }
    .info-box { background: #fff3cd; border: 1px solid #ffc107; padding: 8px; margin-bottom: 12px; border-radius: 4px; }
  </style>
</head>
<body>
  <h1>💰 Expense Tracker — DB Demo</h1>
  <p class="notice">
    <strong>Features:</strong> Stored procedures, triggers (type validation & auto-goal updates), and CASCADE delete demonstration.
  </p>

  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      {% for category, message in messages %}
        <div class="{{ category }}">{{ message }}</div>
      {% endfor %}
    {% endif %}
  {% endwith %}

  <h2>👤 Add User</h2>
  <form method="post" action="{{ url_for('add_user') }}">
    <div class="row">
      <div class="col">
        <label>Name:</label>
        <input name="name" type="text" placeholder="e.g. John Doe" required>
      </div>
      
      <div class="col">
        <label>Email:</label>
        <input name="email" type="email" placeholder="e.g. john@example.com" required>
      </div>
      
      <div class="col">
        <label>Password:</label>
        <input name="password" type="password" placeholder="Enter password" required>
      </div>
    </div>
    <button class="btn" type="submit">➕ Add User</button>
  </form>

  <h2>➕ Add Transaction (Stored Procedure)</h2>
  {% if available_users and available_categories %}
  <form method="post" action="{{ url_for('add_transaction') }}">
    <div class="row">
      <div class="col">
        <label>User:</label>
        <select name="user_id" required>
          <option value="">Select User</option>
          {% for u in available_users %}
          <option value="{{ u.user_id }}">{{ u.name }} (ID: {{ u.user_id }})</option>
          {% endfor %}
        </select>
      </div>
      
      <div class="col">
        <label>Category:</label>
        <select name="category_id" required>
          <option value="">Select Category</option>
          {% for c in available_categories %}
          <option value="{{ c.category_id }}">{{ c.name }} ({{ c.type }})</option>
          {% endfor %}
        </select>
      </div>
      
      <div class="col">
        <label>Amount:</label>
        <input name="amount" type="number" step="0.01" placeholder="e.g. 1500.00" required>
      </div>
      
      <div class="col">
        <label>Type:</label>
        <select name="type" required>
          <option value="income">Income</option>
          <option value="expense" selected>Expense</option>
        </select>
      </div>
      
      <div class="col">
        <label>Date:</label>
        <input name="date" type="date" required>
      </div>
    </div>
    <button class="btn" type="submit">💾 Add Transaction</button>
  </form>
  {% else %}
  <div class="error">⚠️ No users or categories available. Please add them to the database first.</div>
  {% endif %}

  <h2>📊 View Data</h2>
  <form method="get" action="{{ url_for('index') }}">
    <div class="row">
      <label class="col">
        <input type="checkbox" name="show" value="transactions" {% if 'transactions' in show %}checked{% endif %}> 
        Transactions
      </label>
      <label class="col">
        <input type="checkbox" name="show" value="goals" {% if 'goals' in show %}checked{% endif %}> 
        Goals (with auto-update)
      </label>
      <label class="col">
        <input type="checkbox" name="show" value="budgets" {% if 'budgets' in show %}checked{% endif %}> 
        Budgets
      </label>
      <label class="col">
        <input type="checkbox" name="show" value="users" {% if 'users' in show %}checked{% endif %}> 
        Users
      </label>
      <label class="col">
        <input type="checkbox" name="show" value="categories" {% if 'categories' in show %}checked{% endif %}> 
        Categories
      </label>
      <button class="btn" type="submit">🔄 Refresh View</button>
    </div>
  </form>

  {% if transactions %}
    <h3>💳 Transactions</h3>
    <table>
      <tr>
        <th>ID</th><th>User ID</th><th>Category ID</th><th>Amount</th><th>Type</th><th>Date</th>
      </tr>
      {% for t in transactions %}
      <tr>
        <td>{{ t.transaction_id }}</td>
        <td>{{ t.user_id }}</td>
        <td>{{ t.category_id }}</td>
        <td>₹{{ "%.2f"|format(t.amount) }}</td>
        <td>{{ t.type }}</td>
        <td>{{ t.date }}</td>
      </tr>
      {% endfor %}
    </table>
  {% endif %}

  {% if goals %}
    <h3>🎯 Goals (Automatically Updated by Income Trigger)</h3>
    <table>
      <tr>
        <th>ID</th><th>User ID</th><th>Target</th><th>Current</th><th>Progress</th><th>Deadline</th>
      </tr>
      {% for g in goals %}
      <tr>
        <td>{{ g.goal_id }}</td>
        <td>{{ g.user_id }}</td>
        <td>₹{{ "%.2f"|format(g.target_amount) }}</td>
        <td>₹{{ "%.2f"|format(g.current_amount) }}</td>
        <td>{{ "%.1f"|format((g.current_amount / g.target_amount * 100) if g.target_amount > 0 else 0) }}%</td>
        <td>{{ g.deadline or 'N/A' }}</td>
      </tr>
      {% endfor %}
    </table>
  {% endif %}

  {% if budgets %}
    <h3>💰 Budgets</h3>
    <table>
      <tr>
        <th>ID</th><th>User ID</th><th>Category ID</th><th>Limit</th><th>Start Date</th><th>End Date</th>
      </tr>
      {% for b in budgets %}
      <tr>
        <td>{{ b.budget_id }}</td>
        <td>{{ b.user_id }}</td>
        <td>{{ b.category_id }}</td>
        <td>₹{{ "%.2f"|format(b.limit_amount) }}</td>
        <td>{{ b.start_date }}</td>
        <td>{{ b.end_date }}</td>
      </tr>
      {% endfor %}
    </table>
  {% endif %}

  {% if users %}
    <h3>👤 Users (Delete to Demonstrate CASCADE)</h3>
    <div class="info-box">
      ℹ️ Deleting a user will CASCADE delete all their transactions, goals, and budgets.
    </div>
    <table>
      <tr>
        <th>ID</th><th>Name</th><th>Email</th><th>Balance</th><th>Action</th>
      </tr>
      {% for u in users %}
      <tr>
        <td>{{ u.user_id }}</td>
        <td>{{ u.name }}</td>
        <td>{{ u.email }}</td>
        <td>₹{{ "%.2f"|format(u.balance) if u.balance is not none else '0.00' }}</td>
        <td>
          <form method="post" action="{{ url_for('delete_user', user_id=u.user_id) }}" style="display:inline">
            <button class="btn btn-danger" type="submit" 
                    onclick="return confirm('⚠️ Delete {{ u.name }}? This will CASCADE delete all related data!')">
              🗑️ Delete
            </button>
          </form>
        </td>
      </tr>
      {% endfor %}
    </table>
  {% endif %}

  {% if categories %}
    <h3>📁 Categories</h3>
    <table>
      <tr>
        <th>ID</th><th>Name</th><th>Type</th>
      </tr>
      {% for c in categories %}
      <tr>
        <td>{{ c.category_id }}</td>
        <td>{{ c.name }}</td>
        <td>{{ c.type }}</td>
      </tr>
      {% endfor %}
    </table>
  {% endif %}

  <hr>
  <p style="text-align:center; color:#666;">
    <strong>Demo Application</strong> | Stored Procedures ✓ | Triggers ✓ | CASCADE Delete ✓
  </p>
</body>
</html>
"""

# --- Routes ---
@app.route('/', methods=['GET'])
def index():
    show = request.args.getlist('show')
    if not show:
        show = ['transactions', 'users', 'goals']

    data = {
        'transactions': None, 
        'goals': None, 
        'budgets': None, 
        'users': None,
        'categories': None,
        'show': show,
        'available_users': None,
        'available_categories': None
    }
    
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor(dictionary=True)

        # Always fetch users and categories for the form dropdowns
        cur.execute("SELECT user_id, name, email FROM users ORDER BY user_id")
        data['available_users'] = cur.fetchall()
        
        cur.execute("SELECT category_id, name, type FROM categories ORDER BY category_id")
        data['available_categories'] = cur.fetchall()

        if 'transactions' in show:
            cur.execute("SELECT * FROM transactions ORDER BY date DESC LIMIT 200")
            data['transactions'] = cur.fetchall()
            
        if 'goals' in show:
            cur.execute("SELECT * FROM goals ORDER BY goal_id")
            data['goals'] = cur.fetchall()
            
        if 'budgets' in show:
            cur.execute("SELECT * FROM budgets ORDER BY budget_id")
            data['budgets'] = cur.fetchall()
            
        if 'users' in show:
            cur.execute("""
                SELECT 
                    u.user_id, 
                    u.name, 
                    u.email,
                    (SELECT fn_get_user_balance(u.user_id)) as balance
                FROM users u 
                ORDER BY u.user_id
            """)
            data['users'] = cur.fetchall()
            
        if 'categories' in show:
            cur.execute("SELECT * FROM categories ORDER BY category_id")
            data['categories'] = cur.fetchall()

        cur.close()
    except Error as e:
        flash(f"Database error: {e}", 'error')
    finally:
        if conn:
            conn.close()

    return render_template_string(BASE_HTML, **data)

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    # Validation
    if not name or not email or not password:
        flash('Name, Email, and Password are required!', 'error')
        return redirect(url_for('index'))

    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        # Insert the new user with name, email, and password
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        conn.commit()
        
        user_id = cur.lastrowid
        flash(f'✅ User "{name}" (ID: {user_id}) added successfully!', 'success')
        
    except Error as e:
        error_msg = str(e)
        if '1062' in error_msg:
            flash('❌ Email already exists. Please use a different email.', 'error')
        else:
            flash(f'❌ Error adding user: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
            
    return redirect(url_for('index'))

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    user_id = request.form.get('user_id')
    category_id = request.form.get('category_id')
    amount = request.form.get('amount')
    typ = request.form.get('type')
    date = request.form.get('date')

    # Validation
    if not all([user_id, category_id, amount, typ, date]):
        flash('All fields are required!', 'error')
        return redirect(url_for('index'))

    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        # Call the stored procedure
        cur.callproc('sp_add_transaction', (
            int(user_id), 
            int(category_id), 
            float(amount), 
            typ, 
            date
        ))
        conn.commit()

        # Get the inserted transaction ID
        last_id = None
        for res in cur.stored_results():
            rows = res.fetchall()
            if rows:
                last_id = rows[0][0] if isinstance(rows[0], tuple) else rows[0]
        
        flash(f'✅ Transaction #{last_id} added successfully! Triggers executed.', 'success')
        
    except Error as e:
        error_msg = str(e)
        if '1452' in error_msg:
            flash('❌ Invalid User ID or Category ID. Please select from the dropdown.', 'error')
        elif 'does not match category type' in error_msg:
            flash('❌ Transaction type does not match category type. Check your selection!', 'error')
        else:
            flash(f'❌ Error: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
            
    return redirect(url_for('index'))

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute("SELECT name FROM users WHERE user_id = %s", (user_id,))
        user = cur.fetchone()
        
        if not user:
            flash(f'❌ User #{user_id} not found.', 'error')
        else:
            user_name = user[0]
            cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            conn.commit()
            flash(f'✅ User "{user_name}" (ID: {user_id}) deleted successfully! All related data CASCADE deleted.', 'success')
            
    except Error as e:
        flash(f'❌ Error deleting user: {e}', 'error')
    finally:
        if conn:
            conn.close()
            
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)