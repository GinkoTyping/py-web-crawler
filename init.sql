CREATE DATABASE IF NOT EXISTS rental_info;
USE rental_info;

CREATE TABLE IF NOT EXISTS house_info
(
    no       VARCHAR(100) PRIMARY KEY,
    name     VARCHAR(100),
    layout   VARCHAR(50),
    area     VARCHAR(50),
    location VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS agent_info
(
    image_path VARCHAR(100) PRIMARY KEY,
    name       VARCHAR(50),
    company    VARCHAR(50),
    main_area  VARCHAR(50)
)