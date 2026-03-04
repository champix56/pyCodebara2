drop database if exists `cdb`;
create database `cdb`;
create user if not exists `codebara`;
GRANT ALL PRIVILEGES  ON codebara.* TO `codebara`;
GRANT ALL PRIVILEGES  OuserN *.* TO `champix`;
use `cdb`;

create table `user`(id bigint auto_increment primary key, nickname varchar(64),amount int, seed int(3) default 1, mail varchar(128));
create table `card_request`(id bigint auto_increment primary key,userid bigint references user(id), prompt varchar(784 ), request json, daterequest datetime default now(),state int default 0, fileloc varchar(512) );

insert into user values (666,'god', 6666666666, 2,'god@codebara.com' );
INSERT INTO `cdb`.`card_request` (`userid`, `prompt`, `request`, `state`, `fileloc`) VALUES ('666', 'ee', '{"aa":123}', '1', '');

