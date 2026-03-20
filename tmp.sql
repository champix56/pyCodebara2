drop database if exists `cdb`;
create database `cdb`;
create user if not exists `codebara`;
GRANT ALL PRIVILEGES  ON codebara.* TO `codebara`;
GRANT ALL PRIVILEGES  ON *.* TO `champix`;
use `cdb`;

CREATE TABLE `user` (
	`id` BIGINT NOT NULL AUTO_INCREMENT,
	`nickname` VARCHAR(64) NULL DEFAULT NULL ,
	`password` CHAR(64) NOT NULL ,
	`amount` BIGINT NULL DEFAULT NULL,
	`seed` INT NULL DEFAULT '1',
	`mail` VARCHAR(128) NULL DEFAULT NULL ,
	`hash` CHAR(64) AS (sha2(concat(`nickname`,`password`),256)) stored,
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

insert into user values (666,'god', 6666666666, 2,'god@codebara.com' );
INSERT INTO `cdb`.`card` (`ownerid`,`creatorid`, `prompt`, `request`, `state`) VALUES ('666','666', 'ee', '{"aa":123}', '1', '');

