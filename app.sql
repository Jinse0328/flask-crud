-- Active: 1751016462714@@127.0.0.1@3306@crud_db
DROP DATABASE IF EXISTS crud_db;
CREATE DATABASE crud_db DEFAULT CHARACTER SET utf8mb4;
USE crud_db;

CREATE TABLE users(
    num INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    user_id VARCHAR(100) NOT NULL UNIQUE,
    user_pw VARCHAR(100) NOT NULL
);

CREATE TABLE posts(
    num INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    user_name VARCHAR(100) NOT NULL,
    written_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

INSERT INTO users (user_name, date_of_birth, user_id, user_pw)
VALUES
('김ㅇㅇ', '1997-08-23', 'kim12', 'qwe12');

INSERT INTO posts (title, content, user_id, user_name)
VALUES
('예시글', '예시글입니다.', 'kim12', '김ㅇㅇ');