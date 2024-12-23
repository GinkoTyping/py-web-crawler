CREATE DATABASE IF NOT EXISTS rental_info;
USE rental_info;

CREATE TABLE IF NOT EXISTS house_info
(
    no       VARCHAR(50) PRIMARY KEY,
    name     VARCHAR(100),
    layout   VARCHAR(50),
    area     VARCHAR(50),
    location VARCHAR(100)
)