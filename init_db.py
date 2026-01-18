import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123"  # change if your root password is different
)

cursor = db.cursor()

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS chatbot_db")
cursor.execute("USE chatbot_db")

# Drop old tables if they exist
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
cursor.execute("DROP TABLE IF EXISTS messages")
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

# Create users table
cursor.execute("""
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Create messages table
cursor.execute("""
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    message TEXT NOT NULL,
    response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

print("Database and tables created successfully ✅")
db.commit()
cursor.close()
db.close()
