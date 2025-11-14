-- MySQL schema for Disaster Management Education App
CREATE DATABASE IF NOT EXISTS disaster_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE disaster_db;

CREATE TABLE IF NOT EXISTS users (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('student','faculty','admin') NOT NULL DEFAULT 'student'
);

CREATE TABLE IF NOT EXISTS safe_zones (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  latitude DECIMAL(10,7) NOT NULL,
  longitude DECIMAL(10,7) NOT NULL,
  description TEXT
);

CREATE TABLE IF NOT EXISTS disasters (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  disaster_type VARCHAR(100) NOT NULL,
  info TEXT NOT NULL,
  video_link VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS messages (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  sender_id BIGINT NOT NULL,
  receiver_id BIGINT NOT NULL,
  message_text TEXT NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS progress (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL,
  module_name VARCHAR(255) NOT NULL,
  quiz_score INT DEFAULT 0,
  completed BOOLEAN DEFAULT FALSE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
