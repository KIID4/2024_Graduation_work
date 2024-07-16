CREATE TABLE `devices` (
  `device_id` int(11) NOT NULL AUTO_INCREMENT,
  `device_serial` varchar(20) NOT NULL,
  `device_alias` varchar(17) NOT NULL,
  `user_id` varchar(15) NOT NULL,
  PRIMARY KEY (`device_id`),
  KEY `fk_user_id_idx` (`user_id`),
  CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;