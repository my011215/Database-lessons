## sql语句  
1. 网站总表  
```
CREATE TABLE IF NOT EXISTS `website_information`(
   `webname` CHAR(4) PRIMARY KEY,
   `url` CHAR(24) NOT NULL,
   `article_count` SMALLINT NOT NULL,
   `plate_count` TINYINT NOT NULL,
	 `house_location` CHAR(8) NOT NULL,
   `company_name` CHAR(30) NOT NULL,
   `setup_time` YEAR NOT NULL,
   `slogan` CHAR(50) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
2. 搜狐  
```
CREATE TABLE IF NOT EXISTS `souhu_information`(
   `id` TINYINT NOT NULL,
	 `type` CHAR(4) PRIMARY KEY,
   `article_number` SMALLINT NOT NULL,
	 `link` CHAR(50) NOT NULL,
   `child_plate` CHAR(20) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
3. 腾讯  
```
create table if not exists `qq_information`(
`id` TINYINT NOT NULL,
`type` CHAR(4) PRIMARY KEY ,
`article_number` SMALLINT NOT NULL,
`link` CHAR(100) NOT NULL,
`child_plate` CHAR(60) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
4. 新浪  
```
CREATE TABLE IF NOT EXISTS `sina_information`(
   `id` TINYINT NOT NULL,
	 `type` CHAR(4) PRIMARY KEY,
   `article_number` SMALLINT NOT NULL,
	 `link` CHAR(50) NOT NULL,
   `child_plate` CHAR(20) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
5. 网易  
```
CREATE TABLE IF NOT EXISTS `wy_information`(
   `id` TINYINT NOT NULL,
	 `type` CHAR(4) PRIMARY KEY,
   `article_number` SMALLINT NOT NULL,
	 `link` CHAR(50) NOT NULL,
   `child_plate` CHAR(20) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
6. 文章信息  
```
create table if not exists `essay_information`(
`id` smallint not null,
`title` char(76),
`author` char(20),
`source` char(20) not null,
`word_count` smallint not null,
`type` char(4),
`comment_count` smallint not null,
`publish_time` date not null,
`keyword` char(20),
`keyword_count` smallint not null,
`publish_address` char(20),
`article_link` char(150),
primary key(title,article_link),
foreign key(author) references author_information(name),
foreign key(type) references type_information(type),
foreign key(keyword) references key_information(keyword)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

```
7. 关键字信息  
```
create table IF NOT EXISTS `key_information`
(
`id` smallint not null,/*序号*/
`keyword` char(20), /*关键字，主键*/
`keycount` smallint not null,/*关键字总数目*/
`source_article_count` smallint not null, /*来源文章数*/
primary key(`keyword`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
8. 作者信息  
```
CREATE TABLE IF NOT EXISTS `author_information`(
`id` smallint not null,
`name` char(20),
`article_count` int,
`ip_address` char(20),
`introduction` varchar(600),
`fans_number` int,
`source` char(4),
primary key(name,source)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
9. 种类信息  
```
CREATE TABLE IF NOT EXISTS `type_information`
(
`id` tinyint not null,/*序号*/
`type` char(4),/*关键字，主键*/
`article_number` smallint not null,/*关键字总数目*/
primary key(`type`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
10. 热度信息  
```
CREATE TABLE IF NOT EXISTS `hot_spot_information`(
`id` smallint primary key,
`name` char(76),
`rank` smallint not null,
`comment_count` smallint not null,
`type` char(4),
`source` char(20) not null,
foreign key (name) references `essay_information`(title),
foreign key (type) references `type_information`(type)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
### 建表sql语句汇总  
```
CREATE TABLE IF NOT EXISTS `author_information`(
`id` smallint not null,
`name` char(20),
`article_count` int,
`ip_address` char(20),
`introduction` varchar(600),
`fans_number` int,
`source` char(4),
primary key(name,source)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `type_information`
(
`id` tinyint not null,/*序号*/
`type` char(4),/*关键字，主键*/
`article_number` smallint not null,/*关键字总数目*/
primary key(`type`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

create table IF NOT EXISTS `key_information`
(
`id` smallint not null,/*序号*/
`keyword` char(20), /*关键字，主键*/
`keycount` smallint not null,/*关键字总数目*/
`source_article_count` smallint not null, /*来源文章数*/
primary key(`keyword`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

create table if not exists `essay_information`(
`id` smallint not null,
`title` char(76),
`author` char(20),
`source` char(20) not null,
`word_count` smallint not null,
`type` char(4),
`comment_count` smallint not null,
`publish_time` date not null,
`keyword` char(20),
`keyword_count` smallint not null,
`publish_address` char(20),
`article_link` char(150),
primary key(title,article_link),
foreign key(author) references author_information(name),
foreign key(type) references type_information(type),
foreign key(keyword) references key_information(keyword)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `hot_spot_information`(
`id` smallint primary key,
`name` char(76),
`rank` smallint not null,
`comment_count` smallint not null,
`type` char(4),
`source` char(20) not null,
foreign key (name) references `essay_information`(title),
foreign key (type) references `type_information`(type)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `wy_information`(
   `id` TINYINT NOT NULL,
	 `type` CHAR(4) PRIMARY KEY,
   `article_number` SMALLINT NOT NULL,
	 `link` CHAR(50) NOT NULL,
   `child_plate` CHAR(20) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `sina_information`(
   `id` TINYINT NOT NULL,
	 `type` CHAR(4) PRIMARY KEY,
   `article_number` SMALLINT NOT NULL,
	 `link` CHAR(50) NOT NULL,
   `child_plate` CHAR(20) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `website_information`(
   `webname` CHAR(4) PRIMARY KEY,
   `url` CHAR(24) NOT NULL,
   `article_count` SMALLINT NOT NULL,
   `plate_count` TINYINT NOT NULL,
	 `house_location` CHAR(8) NOT NULL,
   `company_name` CHAR(30) NOT NULL,
   `setup_time` YEAR NOT NULL,
   `slogan` CHAR(50) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `souhu_information`(
   `id` TINYINT NOT NULL,
	 `type` CHAR(4) PRIMARY KEY,
   `article_number` SMALLINT NOT NULL,
	 `link` CHAR(50) NOT NULL,
   `child_plate` CHAR(20) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

create table if not exists `qq_information`(
`id` TINYINT NOT NULL,
`type` CHAR(4) PRIMARY KEY ,
`article_number` SMALLINT NOT NULL,
`link` CHAR(100) NOT NULL,
`child_plate` CHAR(60) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
### website_information表sql语句  
```
INSERT INTO `sjk`.`website_information`
VALUES ("新浪网","http://www.sina.com.cn",0,30,"北京","北京新浪互联信息服务有限公司","1998","一切由你开始");
```
```
INSERT INTO `sjk`.`website_information`
VALUES ("网易网","http://www.163.com",0,27,"杭州","网易网络有限公司","1997","网聚人的力量");
```
```
INSERT INTO `sjk`.`website_information`
VALUES ("搜狐网","https://www.sohu.com/",0,21,"北京","北京搜狐互联网信息服务有限公司","1998","上搜狐, 知天下");
```
```
INSERT INTO `sjk`.`website_information`
VALUES ("腾讯网","https://www.qq.com/",0,24,"深圳","深圳市腾讯计算机系统有限公司","1998","一切以用户价值为依归");
```
```
update `website_information` set article_count={counts} where webname='{web_name}网'
```
### key_information表sql语句  
```
INSERT INTO `sjk`.`key_information`(`id`, `keyword`, `keycount`, `source_article_count`) VALUES ({str(i+1)}, '{keyword[i][0]}', {keyword[i][1]}, {keyword[i][2]})
```
```
SELECT keyword from key_information;
```
```
update `key_information` set keycount={count},source_article_count={articles} where keyword='{keys[i][0]}'
```
### author_information表sql语句   
```
INSERT INTO `sjk`.`author_information`(`id`, `name`, `article_count`, `ip_address`, `introduction`, `fans_number`, `source`) VALUES ({str(j)}, '{author[i][0]}', {author[i][1]}, '{author[i][2]}',"{author[i][3]}", {author[i][4]}, '{author[i][5]}')
```
```
UPDATE `sjk`.`author_information` SET `name`='{author[i][0]}',`article_count`={author[i][1]},`ip_address` ='{author[i][2]}', `introduction`='{author[i][3]}', `fans_number`={author[i][4]},`source`='{author[i][5]}' WHERE `name`='{author[i][0]}' AND `source`='{author[i][5]}'
```
```
SELECT name from author_information;
```
```
update `author_information` set article_count={article_count} where name='{auths[i][0]}' 
```
### essay_information表sql语句   
```
INSERT INTO `sjk`.`essay_information`(`id`, `title`, `author`, `source`, `word_count`, `type`, `comment_count`, `publish_time`, `keyword`, `keyword_count`, `publish_address`, `article_link`) VALUES ({str(j)}, '{essay[i][0]}', '{essay[i][1]}', '{essay[i][2]}',{essay[i][3]}, '{essay[i][4]}', {essay[i][5]}, '{essay[i][6]}', '{essay[i][7]}',{essay[i][8]}, '{essay[i][9]}', '{essay[i][10]}')
```
```
select keyword_count from `essay_information` where keyword='{keys[i][0]}' 
```
```
select * from `essay_information` where author='{auths[i][0]}'
```
```
select * from `essay_information` where type='{type_name[i][0]}' and source='{web_name}'
```
```
select * from `essay_information` where type='{type_name[i][0]}'
```
```
SELECT * from `essay_information` where source='{web_name}'
```
```
SELECT title,comment_count,source,type FROM `essay_information` ORDER BY comment_count DESC;
```
### type_information表sql语句   
```
INSERT INTO `sjk`.`type_information` VALUES ({str(j)}, '{types[i][0]}', 0)
```
### wy_information、sina_information、souhu_information、qq_information表sql语句   
```
SELECT type FROM `wy_information` 
UNION SELECT type from `qq_information`
UNION SELECT type from `sina_information`
UNION SELECT type from `souhu_information`
```
```
INSERT INTO `sjk`.`{web}_information`(`id`, `type`, `article_number`, `link`, `child_plate`) VALUES ({i}, '{li[0]}', '{li[1]}', '{li[2]}', '{li[3]}')
```
```
update `{web}_information` set article_number={counts} where type='{type_name[i][0]}'
```
### hot_spot_information表sql语句   
```
INSERT INTO `sjk`.`hot_spot_information` (`id`,`name`,`comment_count`,`source`,`type`,`rank`) VALUES ({str(i+1)}, '{essays[i][0]}',{essays[i][1]},'{essays[i][2]}','{essays[i][3]}',{j})
```

                  