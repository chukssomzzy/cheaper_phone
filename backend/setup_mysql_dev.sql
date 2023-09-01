-- Setup Database for development 

CREATE DATABASE IF NOT EXISTS `ECOMMERCE_DB`;
CREATE USER IF NOT EXISTS 'ECOMMERCE_DB_USER'@'localhost' IDENTIFIED BY 'ecommerce_DB_USER_PWD1';
GRANT ALL PRIVILEGES ON `ECOMMERCE_DB`.* TO 'ECOMMERCE_DB_USER'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'ECOMMERCE_DB_USER'@'localhost';
FLUSH PRIVILEGES;
