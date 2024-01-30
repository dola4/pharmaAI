CREATE DATABASE IF NOT EXISTS pharmaai;

USE pharmaai;

CREATE TABLE IF NOT EXISTS drugs (
    drug_id INT AUTO_INCREMENT PRIMARY KEY,
    mongo_id VARCHAR(24),
    name VARCHAR(255),
    stock INT,
    buy_price DECIMAL(10, 2),
    sell_price DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS clients (
    client_id INT AUTO_INCREMENT PRIMARY KEY,
    mongo_id VARCHAR(24),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    age INT,
    sexe CHAR(1),
    email VARCHAR(255),
    phone VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS adresses (
    address_id INT AUTO_INCREMENT PRIMARY KEY,
    mongo_id VARCHAR(24),
    door INT,
    street VARCHAR(255),
    city VARCHAR(255),
    postal_code VARCHAR(20),
    state VARCHAR(255),
    country VARCHAR(255),
    client_id INT,
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
);

CREATE TABLE IF NOT EXISTS client_addresses (
    client_id INT,
    address_id INT,
    PRIMARY KEY (client_id, address_id),
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (address_id) REFERENCES adresses(address_id)
);

CREATE TABLE IF NOT EXISTS prescriptions (
    prescription_id INT AUTO_INCREMENT PRIMARY KEY,
    mongo_id VARCHAR(24),
    client_id INT,
    drug_id INT,
    given_date DATE,
    expiration_date DATE,
    hospital VARCHAR(255),
    doctor VARCHAR(255),
    status VARCHAR(255),
    max_given INT,
    given_nb INT,
    FOREIGN KEY (drug_id) REFERENCES drugs(drug_id),
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
);

CREATE TABLE IF NOT EXISTS sells (
    sell_id INT AUTO_INCREMENT PRIMARY KEY,
    mongo_id VARCHAR(24),
    date DATE,
    client_id INT,
    total DECIMAL(10, 2),
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
);

CREATE TABLE IF NOT EXISTS sell_prescriptions (
    sell_id INT,
    prescription_id INT,
    FOREIGN KEY (sell_id) REFERENCES sells(sell_id),
    FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id)
);

