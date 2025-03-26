

ALTER USER 'admin'@'%' IDENTIFIED BY '';

FLUSH PRIVILEGES;

-- Create a fake financial records table
CREATE TABLE financial_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    account_number VARCHAR(20) NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_amount DECIMAL(10, 2) NOT NULL,
    transaction_type ENUM('Credit', 'Debit') NOT NULL,
    balance DECIMAL(10, 2) NOT NULL,
    notes VARCHAR(255)
);

-- Insert fake data into the table
INSERT INTO financial_records (customer_name, account_number, transaction_date, transaction_amount, transaction_type, balance, notes) VALUES
('John Doe', '1234567890', '2024-10-15', 1500.00, 'Credit', 2500.00, 'Monthly salary deposit'),
('Jane Smith', '9876543210', '2024-10-20', 200.00, 'Debit', 2300.00, 'ATM withdrawal'),
('Alice Johnson', '4567891230', '2024-11-01', 5000.00, 'Credit', 7300.00, 'Tax refund'),
('Bob Brown', '7891234560', '2024-11-03', 1200.00, 'Debit', 6100.00, 'Online purchase'),
('Charlie White', '3216549870', '2024-11-04', 1000.00, 'Credit', 7100.00, 'Bonus deposit'),
('Diana Evans', '6549873210', '2024-11-04', 300.00, 'Debit', 6800.00, 'Utility bill payment');
