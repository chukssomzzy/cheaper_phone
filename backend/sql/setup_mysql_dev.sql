-- Setup Database for development 

CREATE DATABASE IF NOT EXISTS `cheaper_phone_db`;
CREATE USER IF NOT EXISTS 'cheaper_phone_db_user'@'localhost' IDENTIFIED BY 'cheaper_phone_db_PWD12#';
GRANT ALL PRIVILEGES ON `cheaper_phone_db`.* TO 'cheaper_phone_db_user'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'cheaper_phone_db_user'@'localhost';
FLUSH PRIVILEGES;
