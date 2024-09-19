CREATE DATABASE IF NOT EXISTS Airflow;
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

Create Database IF NOT EXISTS Attendence_System;
use Attendence_System;
CREATE TABLE IF NOT EXISTS raw (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    emp_id VARCHAR(255),
    team_manager_id INT,
    designation_id INT,
    designation_name VARCHAR(255),
    first_name VARCHAR(255),
    middle_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    is_hr VARCHAR(255),
    is_supervisor VARCHAR(255),
    leave_issuer_id INT,
    issuer_first_name VARCHAR(255),
    issuer_middle_name VARCHAR(255),
    issuer_last_name VARCHAR(255),
    current_leave_issuer_id INT,
    current_leave_issuer_email VARCHAR(255),
    department_description VARCHAR(255),
    start_date DATE,
    end_date DATE,
    leave_days INT,
    reason TEXT,
    leave_status VARCHAR(255),
    status VARCHAR(255),
    response_remarks TEXT,
    leave_type_id INT,
    leave_type VARCHAR(255),
    default_days INT,
    transferable_days INT,
    is_consecutive VARCHAR(255),
    fiscal_id INT,
    fiscal_start_date DATE,
    fiscal_end_date DATE,
    fiscal_is_current VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    is_automated VARCHAR(255),
    is_converted VARCHAR(255),
    total_count INT,
    inserted_at DATE,
    allocations TEXT
);
drop table if exist users;
CREATE TABLE IF NOT EXISTS employee (
    id INT AUTO_INCREMENT PRIMARY KEY,
    emp_id VARCHAR(50),
    first_name VARCHAR(100),
    middle_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    designation_id INT,
    designation_name VARCHAR(100),
    department_description VARCHAR(255),
    is_hr BOOLEAN,
    is_supervisor BOOLEAN
);

CREATE TABLE IF NOT EXISTS leaves (
    id INT AUTO_INCREMENT PRIMARY KEY,
    leave_type VARCHAR(100),
    default_days INT,
    transferable_days INT,
    fiscal_id INT,
    fiscal_start_date DATE,
    fiscal_end_date DATE,
    fiscal_is_current BOOLEAN
);

CREATE TABLE IF NOT EXISTS leave_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    leave_type_id INT,
    start_date DATE,
    end_date DATE,
    leave_days INT,
    reason VARCHAR(255),
    response_remarks VARCHAR(255),
    leave_status VARCHAR(50),
    is_converted BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    current_leave_issuer_id INT,
    issuer_first_name VARCHAR(100),
    issuer_middle_name VARCHAR(100),
    issuer_last_name VARCHAR(100),
    current_leave_issuer_email VARCHAR(100),
    is_consecutive BOOLEAN,
    is_automated BOOLEAN,
    department_description VARCHAR(100),
    designation_name VARCHAR(100),
    designation_id int,
    is_supervisor BOOLEAN,
    is_hr BOOLEAN
);

CREATE TABLE designation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    designation_name VARCHAR(255) NOT NULL
);


CREATE TABLE Status (
    id INT PRIMARY KEY AUTO_INCREMENT,
    status_type VARCHAR(255) NOT NULL,
    start_date DATE NULL,
    end_date DATE NULL,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);



