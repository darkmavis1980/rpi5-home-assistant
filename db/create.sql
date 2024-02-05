CREATE DATABASE templogs;

CREATE TABLE `measurements` (
  id INT NOT NULL auto_increment AUTO_INCREMENT,
  `temperature` DECIMAL(10,2) DEFAULT 0 NOT NULL,
  `humidity` DECIMAL(10,2) DEFAULT 0 NOT NULL,
  `pressure` DECIMAL(10,2) DEFAULT 0 NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `room_id` INT DEFAULT 1 NOT NULL,
  PRIMARY KEY (`id`)
);

ALTER TABLE measurements ADD FOREIGN KEY (room_id) REFERENCES rooms(id);

CREATE TABLE `rooms` (
  id INT NOT NULL auto_increment AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `label` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

INSERT INTO `rooms` (name, label) VALUES ('office', 'Office');
