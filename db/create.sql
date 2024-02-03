CREATE DATABASE templogs;

CREATE TABLE `measurements` (
  id INT NOT NULL auto_increment AUTO_INCREMENT,
  `temperature` DECIMAL DEFAULT 0.0 NOT NULL,
  `humidity` DECIMAL DEFAULT 0.0 NOT NULL,
  `pressure` DECIMAL DEFAULT 0.0 NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

CREATE TABLE `rooms` (
  id INT NOT NULL auto_increment AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `label` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

ALTER TABLE `measurements` ADD `room_id` INT NULL;

UPDATE `measurements` SET room_id = 1;

INSERT INTO `rooms` (name, label) VALUES ('office', 'Office');

ALTER TABLE measurements ADD FOREIGN KEY (room_id) REFERENCES rooms(id);