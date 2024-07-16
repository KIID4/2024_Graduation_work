CREATE TABLE `users` (
  `user_id` varchar(15) NOT NULL,
  `user_password` varchar(200) NOT NULL,
  `user_nickname` varchar(80) NOT NULL,
  `user_phone_number` varchar(13) NOT NULL,
  `user_email` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `uq_user_user_nickname` (`user_nickname`),
  UNIQUE KEY `uq_user_user_phone_number` (`user_phone_number`),
  UNIQUE KEY `uq_user_user_email` (`user_email`),
  CONSTRAINT `CONSTRAINT_1` CHECK (octet_length(`user_id`) >= 4),
  CONSTRAINT `CONSTRAINT_2` CHECK (octet_length(`user_password`) >= 4),
  CONSTRAINT `CONSTRAINT_3` CHECK (octet_length(`user_nickname`) >= 2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;