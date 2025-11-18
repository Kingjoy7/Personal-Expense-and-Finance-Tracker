CREATE DATABASE expense_tracker;
USE expense_tracker;

CREATE TABLE users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);


CREATE TABLE categories (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  type ENUM('income','expense') NOT NULL
);


CREATE TABLE transactions (
  transaction_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  category_id INT NOT NULL,
  amount DECIMAL(12,2) NOT NULL CHECK (amount > 0),
  type ENUM('income','expense') NOT NULL,
  date DATE NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);


DELIMITER $$

CREATE TRIGGER check_transaction_type
BEFORE INSERT ON transactions
FOR EACH ROW
BEGIN
  DECLARE cat_type ENUM('income','expense');
  SELECT type INTO cat_type FROM categories WHERE category_id = NEW.category_id;
  IF cat_type <> NEW.type THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Transaction type does not match category type';
  END IF;
END$$

DELIMITER ;


CREATE TABLE goals (
  goal_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  target_amount DECIMAL(12,2) NOT NULL CHECK (target_amount > 0),
  current_amount DECIMAL(12,2) NOT NULL CHECK (current_amount >= 0),
  deadline DATE,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  CHECK (current_amount <= target_amount)
);


CREATE TABLE budgets (
  budget_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  category_id INT NOT NULL,
  limit_amount DECIMAL(12,2) NOT NULL CHECK (limit_amount > 0),
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (category_id) REFERENCES categories(category_id),
  CHECK (start_date <= end_date)
);


INSERT INTO users (name, email, password) VALUES
('Alice Kumar', 'alice@example.com', '1234'),
('Bob Singh', 'bob@example.com', 'abcd');

INSERT INTO categories (name, type) VALUES
('Salary', 'income'),
('Gift', 'income'),
('Groceries', 'expense'),
('Rent', 'expense'),
('Entertainment', 'expense');

INSERT INTO transactions (user_id, category_id, amount, type, date) VALUES
(1, 1, 50000.00, 'income', '2025-08-01'),
(1, 3, 1500.00, 'expense', '2025-08-03'),
(2, 4, 8000.00, 'expense', '2025-08-05'),
(2, 2, 2000.00, 'income', '2025-08-10'),
(1, 5, 500.00, 'expense', '2025-08-15');

INSERT INTO goals (user_id, target_amount, current_amount, deadline) VALUES
(1, 20000.00, 5000.00, '2026-06-30'),
(2, 50000.00, 12000.00, '2026-12-31');

INSERT INTO budgets (user_id, category_id, limit_amount, start_date, end_date) VALUES
(1, 3, 6000.00, '2025-08-01', '2025-08-31'),
(2, 5, 2000.00, '2025-08-01', '2025-08-31');
SELECT * FROM users;
SELECT * FROM categories;
SELECT * FROM transactions;
SELECT * FROM goals;
SELECT * FROM budgets;
