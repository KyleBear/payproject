-- SQL --

CREATE TABLE Owner (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone_number VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE Product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    cost_price DECIMAL(10, 2) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    barcode VARCHAR(255),
    expiration_date DATE,
    size ENUM('small', 'large') NOT NULL,
    owner_id INT,
    FOREIGN KEY (owner_id) REFERENCES Owner(id)
);
