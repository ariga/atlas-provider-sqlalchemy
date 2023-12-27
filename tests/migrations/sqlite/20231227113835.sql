-- Create "user_account" table
CREATE TABLE `user_account` (
  `id` integer NOT NULL,
  `name` varchar NOT NULL,
  `fullname` varchar NULL,
  PRIMARY KEY (`id`)
);
-- Create "address" table
CREATE TABLE `address` (
  `id` integer NOT NULL,
  `email_address` varchar NOT NULL,
  `user_id` integer NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `0` FOREIGN KEY (`user_id`) REFERENCES `user_account` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
);
