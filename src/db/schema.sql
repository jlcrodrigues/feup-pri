DROP SCHEMA IF EXISTS pri_g81 CASCADE;

CREATE SCHEMA pri_g81;

CREATE TABLE dummy_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    email VARCHAR(255)
);

INSERT INTO dummy_table (name, age, email) VALUES
    ('John Doe', 30, 'johndoe@example.com'),
    ('Jane Smith', 25, 'janesmith@example.com'),
    ('Bob Johnson', 35, 'bob@example.com'),
    ('Alice Williams', 28, 'alice@example.com');