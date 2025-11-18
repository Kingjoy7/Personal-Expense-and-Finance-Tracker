USE expense_tracker;

DROP TRIGGER IF EXISTS check_transaction_type;
DROP TRIGGER IF EXISTS check_transaction_type_before_insert;
DROP TRIGGER IF EXISTS check_transaction_type_before_update;
DROP TRIGGER IF EXISTS apply_income_to_goal_after_insert;
DROP PROCEDURE IF EXISTS sp_add_transaction;
DROP FUNCTION IF EXISTS fn_get_user_balance;


DELIMITER $$

CREATE TRIGGER check_transaction_type_before_insert
BEFORE INSERT ON transactions
FOR EACH ROW
BEGIN
  DECLARE cat_type ENUM('income','expense');
  SELECT type INTO cat_type FROM categories WHERE category_id = NEW.category_id;
  IF cat_type <> NEW.type THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Transaction type does not match category type';
  END IF;
END$$

CREATE TRIGGER check_transaction_type_before_update
BEFORE UPDATE ON transactions
FOR EACH ROW
BEGIN
  DECLARE cat_type ENUM('income','expense');
  IF NEW.category_id IS NOT NULL THEN
    SELECT type INTO cat_type FROM categories WHERE category_id = NEW.category_id;
    IF cat_type <> NEW.type THEN
      SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Updated transaction type does not match updated category type';
    END IF;
  END IF;
END$$

CREATE TRIGGER apply_income_to_goal_after_insert
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
  DECLARE v_goal_id INT;
  IF NEW.type = 'income' THEN
    SELECT goal_id INTO v_goal_id
    FROM goals
    WHERE user_id = NEW.user_id
      AND current_amount < target_amount
      AND (deadline IS NULL OR deadline >= NEW.date)
    ORDER BY deadline IS NULL, deadline ASC
    LIMIT 1;
    
    IF v_goal_id IS NOT NULL THEN
      UPDATE goals
      SET current_amount = LEAST(target_amount, current_amount + NEW.amount)
      WHERE goal_id = v_goal_id;
    END IF;
  END IF;
END$$

CREATE PROCEDURE sp_add_transaction(
  IN p_user_id INT,
  IN p_category_id INT,
  IN p_amount DECIMAL(12,2),
  IN p_type VARCHAR(10),
  IN p_date DATE
)
BEGIN
  IF p_amount <= 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Amount must be > 0';
  END IF;
  
  INSERT INTO transactions (user_id, category_id, amount, type, date)
  VALUES (p_user_id, p_category_id, p_amount, p_type, p_date);
  
  SELECT LAST_INSERT_ID() AS transaction_id;
END$$

CREATE FUNCTION fn_get_user_balance(p_user_id INT)
RETURNS DECIMAL(14,2)
DETERMINISTIC
BEGIN
  DECLARE v_income DECIMAL(14,2) DEFAULT 0.00;
  DECLARE v_expense DECIMAL(14,2) DEFAULT 0.00;
  
  SELECT IFNULL(SUM(amount),0.00) INTO v_income
  FROM transactions
  WHERE user_id = p_user_id AND type = 'income';
  
  SELECT IFNULL(SUM(amount),0.00) INTO v_expense
  FROM transactions
  WHERE user_id = p_user_id AND type = 'expense';
  
  RETURN v_income - v_expense;
END$$

DELIMITER ;

SELECT 'Users:' AS Info;
SELECT * FROM users;

SELECT 'Categories:' AS Info;
SELECT * FROM categories;