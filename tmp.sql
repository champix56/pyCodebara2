drop database if exists `cdb`;
create database `cdb`;
create user if not exists `codebara`;
GRANT ALL PRIVILEGES  ON codebara.* TO `codebara`;
GRANT ALL PRIVILEGES  ON *.* TO `champix`;
use `cdb`;


DROP TABLE IF EXISTS user;

DROP TABLE IF EXISTS user;
CREATE TABLE `user` (
	`id` BIGINT NOT NULL AUTO_INCREMENT,
	`nickname` VARCHAR(64) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`password` CHAR(64) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`amount` BIGINT NULL DEFAULT 0,
	`seed` INT NOT NULL DEFAULT (lpad(((rand() * 10 )+1)% 6, 1, '0')),
	`mail` VARCHAR(128) NULL DEFAULT NULL UNIQUE COLLATE  'utf8mb4_0900_ai_ci',
	`API_request_token` VARCHAR(64) NULL,
	`API_token` VARCHAR(64)  NULL ,
	`hash` CHAR(64) NULL,
	PRIMARY KEY (`id`)
);
CREATE TABLE `card` (
	`id` BIGINT NOT NULL AUTO_INCREMENT,
	`creatorid` BIGINT NULL DEFAULT NULL  REFERENCES `user` (`id`) ON UPDATE NO ACTION ON DELETE SET NULL,
    `ownerid`  BIGINT NULL DEFAULT NULL  REFERENCES `user` (`id`) ON UPDATE NO ACTION ON DELETE SET NULL,
    `seasonid` INT NOT NULL ,
	`prompt` VARCHAR(784) NULL DEFAULT NULL ,
    `seasonPromptid` varchar(16) NULL default NULL,
	`request` JSON NULL DEFAULT NULL,
	`daterequest` DATETIME NULL DEFAULT (CURRENT_TIMESTAMP),
	`state` INT NULL DEFAULT '1',
	`fileloc` VARCHAR(512) NULL DEFAULT NULL,
	`cardHash` CHAR(64) NULL DEFAULT NULL,
	`name` varchar(96) NOT NULL DEFAULT '',
	`health` INT NOT NULL DEFAULT 0,
	`attack` INT NOT NULL DEFAULT 0,
    `cardpower` INTEGER NOT NULL DEFAULT 100,
	PRIMARY KEY (`id`)
);
INSERT INTO user(`id`,`nickname`,`password`,`amount`,`mail`,`hash`) values (666,'god',SHA2('god@codebara.comazerty',256), 6666666666, 'god@codebara.com',SHA2('god',256) );
INSERT INTO `cdb`.`card` (`ownerid`,`creatorid`, `prompt`, `request`, `state`) VALUES ('666','666', 'ee', '{"aa":123}', '1', '');

