-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'card'
-- 
-- ---

drop database if exists `codebara`;
create database `codebara`;
create user if not exists `codebara`;
 GRANT ALL PRIVILEGES  ON codebara.* TO `codebara`;
 GRANT ALL PRIVILEGES  ON *.* TO `champix`;

use `codebara`;


DROP TABLE IF EXISTS `card`;
		
CREATE TABLE `card` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `id_user_creator` BIGINT NULL DEFAULT NULL,
  `name` VARCHAR(48) NULL DEFAULT '""',
  `attack` INTEGER NULL DEFAULT 0,
  `heart` INTEGER NULL DEFAULT 0,
  `id_user_owner` BIGINT NULL DEFAULT NULL,
  `id_saison` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'saison'
-- 
-- ---

DROP TABLE IF EXISTS `saison`;
		
CREATE TABLE `saison` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `start_date` DATE NULL DEFAULT NULL,
  `end_date` INTEGER NULL DEFAULT NULL,
  `backscreen` BLOB NULL DEFAULT NULL,
  `name` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'user'
-- 
-- ---

DROP TABLE IF EXISTS `user`;
		
CREATE TABLE `user` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(96) NOT NULL UNIQUE DEFAULT 'NULL',
  `nickname` VARCHAR(48) NOT NULL UNIQUE DEFAULT 'NULL',
  `password` CHAR(64) NOT NULL DEFAULT 'NULL',
  `last_token` CHAR(64) NULL DEFAULT NULL,
  `seed` INTEGER NOT NULL DEFAULT 0,
  `amount` INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'face'
-- 
-- ---

DROP TABLE IF EXISTS `face`;
		
CREATE TABLE `face` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `type` INTEGER NULL DEFAULT NULL,
  `id_saison` INTEGER NOT NULL,
  `image` BLOB NULL DEFAULT NULL,
  `filename` VARCHAR(128) NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'word'
-- 
-- ---

DROP TABLE IF EXISTS `word`;
		
CREATE TABLE `word` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `id_saison` INTEGER NULL,
  `value` VARCHAR(64) NULL DEFAULT NULL,
  `position` INTEGER NULL DEFAULT 4,
  `id_wordtype` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'word_type'
-- 
-- ---

DROP TABLE IF EXISTS `word_type`;
		
CREATE TABLE `word_type` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(32) NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'screencomponent'
-- 
-- ---

DROP TABLE IF EXISTS `screencomponent`;
		
CREATE TABLE `screencomponent` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `id_saison` INTEGER NOT NULL,
  `x` INTEGER NOT NULL DEFAULT 0,
  `y` INTEGER NOT NULL DEFAULT 0,
  `w` INTEGER NOT NULL DEFAULT 10,
  `image` BLOB NOT NULL,
  PRIMARY KEY (`id`, `id_saison`)
);

-- ---
-- Table 'facecomponent'
-- 
-- ---

DROP TABLE IF EXISTS `facecomponent`;
		
CREATE TABLE `facecomponent` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `id_face` INTEGER NOT NULL,
  `x` INTEGER NULL DEFAULT 0,
  `y` INTEGER NULL DEFAULT NULL,
  `w` INTEGER NULL DEFAULT NULL,
  `h` INTEGER NULL DEFAULT NULL,
  `type` CHAR(12) NOT NULL DEFAULT 'text',
  `ressource` BLOB NULL DEFAULT NULL,
  PRIMARY KEY (`id`, `id_face`)
);

-- ---
-- Table 'transaction'
-- 
-- ---

DROP TABLE IF EXISTS `transaction`;
		
CREATE TABLE `transaction` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `id_user` BIGINT NULL DEFAULT NULL,
  `amount` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table 'transaction_card'
-- 
-- ---

DROP TABLE IF EXISTS `transaction_card`;
		
CREATE TABLE `transaction_card` (
  `id` INTEGER NOT NULL AUTO_INCREMENT,
  `id_seller` BIGINT NULL DEFAULT NULL,
  `id_buyer` BIGINT NULL DEFAULT NULL,
  `id_card` BIGINT NULL DEFAULT NULL,
  `date` TIMESTAMP NOT NULL DEFAULT now(),
  `amount` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Foreign Keys 
-- ---

ALTER TABLE `card` ADD FOREIGN KEY (id_user_creator) REFERENCES `user` (`id`);
ALTER TABLE `card` ADD FOREIGN KEY (id_user_owner) REFERENCES `user` (`id`);
ALTER TABLE `card` ADD FOREIGN KEY (id_saison) REFERENCES `saison` (`id`);
ALTER TABLE `word` ADD FOREIGN KEY  (id_saison) REFERENCES `saison`(`id`);
ALTER TABLE `face` ADD FOREIGN KEY (id_saison) REFERENCES `saison` (`id`);
ALTER TABLE `word` ADD FOREIGN KEY (id_wordtype) REFERENCES `word_type` (`id`);
ALTER TABLE `screencomponent` ADD FOREIGN KEY (id_saison) REFERENCES `saison` (`id`);
ALTER TABLE `facecomponent` ADD FOREIGN KEY (id_face) REFERENCES `face` (`id`);
ALTER TABLE `transaction` ADD FOREIGN KEY (id_user) REFERENCES `user` (`id`);
ALTER TABLE `transaction_card` ADD FOREIGN KEY (id_seller) REFERENCES `user` (`id`);
ALTER TABLE `transaction_card` ADD FOREIGN KEY (id_buyer) REFERENCES `user` (`id`);
ALTER TABLE `transaction_card` ADD FOREIGN KEY (id_card) REFERENCES `card` (`id`);

-- ---
-- Table Properties
-- ---

-- ALTER TABLE `card` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `saison` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `user` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `face` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `word` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `word_type` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `screencomponent` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `facecomponent` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `transaction` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `transaction_card` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `card` (`id`,`id_user_creator`,`name`,`attack`,`heart`,`id_user_owner`,`id_saison`) VALUES
-- ('','','','','','','');
-- INSERT INTO `saison` (`id`,`start_date`,`end_date`,`backscreen`,`name`) VALUES
-- ('','','','','');
-- INSERT INTO `user` (`id`,`email`,`nickname`,`password`,`last_token`,`seed`,`amount`) VALUES
-- ('','','','','','','');
-- INSERT INTO `face` (`id`,`type`,`id_saison`,`image`,`filename`) VALUES
-- ('','','','','');
-- INSERT INTO `word` (`id`,`id_saison`,`value`,`position`,`id_wordtype`) VALUES
-- ('','','','','');
-- INSERT INTO `word_type` (`id`,`name`) VALUES
-- ('','');
-- INSERT INTO `screencomponent` (`id`,`id_saison`,`x`,`y`,`w`,`image`) VALUES
-- ('','','','','','');
-- INSERT INTO `facecomponent` (`id`,`id_face`,`x`,`y`,`w`,`h`,`type`,`ressource`) VALUES
-- ('','','','','','','','');
-- INSERT INTO `transaction` (`id`,`id_user`,`amount`) VALUES
-- ('','','');
-- INSERT INTO `transaction_card` (`id`,`id_seller`,`id_buyer`,`id_card`,`date`,`amount`) VALUES
-- ('','','','','','');
INSERT INTO `user` (`email`, `nickname`, `password`, `last_token`, `seed`, `amount`) VALUES ( 'a@', 'champ', 'kjijij', NULL, '0', '0');