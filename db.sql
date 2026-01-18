CREATE DATABASE chatbot_db;

USE chatbot_db;

CREATE TABLE chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_message VARCHAR(255),
    bot_reply VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
