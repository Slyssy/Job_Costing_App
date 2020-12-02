-- project details 
CREATE TABLE project_details(
    project_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(50),
    street VARCHAR(50),
    street2 VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(2),
    zip VARCHAR(5),
    revenue float,
    est_labor_rate FLOAT,
    est_labor_hours FLOAT,
    est_labor_expense FLOAT,
    act_start_date DATE, 
    act_comp_date DATE
);

-- users 
CREATE TABLE users(
    user_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    job_title VARCHAR(50),
    pay_rate FLOAT,
    name VARCHAR(50),
    email VARCHAR(30),
    phone VARCHAR(20),
    log_in VARCHAR(30),
    password VARCHAR(30)
);

-- time sheets
CREATE TABLE time_sheets(
    time_sheet_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id INTEGER REFERENCES users(user_id),
    project_id INTEGER REFERENCES project_details(project_id),
    start_time timestamp, 
    finish_time timestamp
);

-- progress reports
CREATE TABLE progress_reports(
    progress_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    project_id INTEGER REFERENCES project_details(project_id),
    user_id INTEGER REFERENCES users(user_id),
    log_date DATE, 
    percent_complete FLOAT
);
