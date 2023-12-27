-- Create "user_account" table
CREATE TABLE `user_account` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `fullname` varchar(30) NULL,
  PRIMARY KEY (`id`)
) CHARSET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
-- Create "address" table
CREATE TABLE `address` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email_address` varchar(30) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `user_id` (`user_id`),
  CONSTRAINT `address_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_account` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
) CHARSET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
