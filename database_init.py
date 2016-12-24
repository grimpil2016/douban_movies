# -*- coding:utf-8 -*-

import pymysql

class TableCreator(object):

	def __init__(self):

		#连接数据库
		self.conn = pymysql.connect(host='localhost', user='root', password='r00t2oi6',db='douban_movies', port=3306, charset='utf8')
		self.cur = self.conn.cursor()

		#创建17个表
		self.create()

	def create(self):
		#创建各个表
		self.cur.execute('''
			-- -----------------------------------------------------
			-- Table `douban_movies`.`movies`
			-- -----------------------------------------------------
			DROP TABLE IF EXISTS `douban_movies`.`movies` ;

			CREATE TABLE IF NOT EXISTS `douban_movies`.`movies` (
			  `douban_id` INT NOT NULL AUTO_INCREMENT,
			  `imdb_id` VARCHAR(16) NULL,
			  `title` VARCHAR(256) NULL,
			  `year` INT NULL,
			  `runtime` VARCHAR(512) NULL,
			  `release_time` VARCHAR(512) NULL,
			  `other_names` VARCHAR(512) NULL,
			  `summary` VARCHAR(2048) NULL,
			  `watched_num` INT NULL,
			  `to_watch_num` INT NULL,
			  `comments_num` INT NULL,
			  `reviews_num` INT NULL,
			  `questions_num` INT NULL,
			  `img_url` VARCHAR(256) NULL,
			  `website` VARCHAR(256) NULL,
			  PRIMARY KEY (`douban_id`),
			  UNIQUE INDEX `douban_id_UNIQUE` (`douban_id` ASC))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `douban_movies`.`directors`
			-- -----------------------------------------------------
			DROP TABLE IF EXISTS `douban_movies`.`directors` ;

			CREATE TABLE IF NOT EXISTS `douban_movies`.`directors` (
			  `director_id` INT NOT NULL AUTO_INCREMENT,
			  `director_douban_id` INT NULL,
			  `director_name` VARCHAR(64) NULL,
			  UNIQUE INDEX `director_id_UNIQUE` (`director_id` ASC),
			  PRIMARY KEY (`director_id`))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `douban_movies`.`writers`
			-- -----------------------------------------------------
			DROP TABLE IF EXISTS `douban_movies`.`writers` ;

			CREATE TABLE IF NOT EXISTS `douban_movies`.`writers` (
			  `writer_id` INT NOT NULL AUTO_INCREMENT,
			  `writer_douban_id` INT NULL,
			  `writer_name` VARCHAR(64) NULL,
			  PRIMARY KEY (`writer_id`),
			  UNIQUE INDEX `writer_id_UNIQUE` (`writer_id` ASC))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `douban_movies`.`stars`
			-- -----------------------------------------------------
			DROP TABLE IF EXISTS `douban_movies`.`stars` ;

			CREATE TABLE IF NOT EXISTS `douban_movies`.`stars` (
			  `star_id` INT NOT NULL AUTO_INCREMENT,
			  `star_douban_id` INT NULL,
			  `star_name` VARCHAR(64) NULL,
			  PRIMARY KEY (`star_id`),
			  UNIQUE INDEX `star_id_UNIQUE` (`star_id` ASC))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `douban_movies`.`genres`
			-- -----------------------------------------------------
			DROP TABLE IF EXISTS `douban_movies`.`genres` ;

			CREATE TABLE IF NOT EXISTS `douban_movies`.`genres` (
			  `genre_id` INT NOT NULL AUTO_INCREMENT,
			  `genre` VARCHAR(64) NULL,
			  PRIMARY KEY (`genre_id`),
			  UNIQUE INDEX `genre_UNIQUE` (`genre` ASC))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `douban_movies`.`locations`
			-- -----------------------------------------------------
			DROP TABLE IF EXISTS `douban_movies`.`locations` ;

			CREATE TABLE IF NOT EXISTS `douban_movies`.`locations` (
			  `location_id` INT NOT NULL AUTO_INCREMENT,
			  `location` VARCHAR(64) NULL,
			  PRIMARY KEY (`location_id`),
			  UNIQUE INDEX `location_id_UNIQUE` (`location_id` ASC),
			  UNIQUE INDEX `location_UNIQUE` (`location` ASC))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `douban_movies`.`languages`
			-- -----------------------------------------------------
			DROP TABLE IF EXISTS `douban_movies`.`languages` ;

			CREATE TABLE IF NOT EXISTS `douban_movies`.`languages` (
			  `language_id` INT NOT NULL AUTO_INCREMENT,
			  `language` VARCHAR(64) NULL,
			  PRIMARY KEY (`language_id`),
			  UNIQUE INDEX `language_UNIQUE` (`language` ASC))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `douban_movies`.`rate`
			-- -----------------------------------------------------
			DROP TABLE IF EXISTS `douban_movies`.`rate` ;

			CREATE TABLE IF NOT EXISTS `douban_movies`.`rate` (
			  `douban_id` INT NOT NULL,
			  `rate` FLOAT NULL,
			  `rate_num` INT NULL,
			  `rate_per_5stars` FLOAT NULL,
			  `rate_per_4stars` FLOAT NULL,
			  `rate_per_3stars` FLOAT NULL,
			  `rate_per_2stars` FLOAT NULL,
			  `rate_per_1star` FLOAT NULL,
			  PRIMARY KEY (`douban_id`),
			  UNIQUE INDEX `douban_id_UNIQUE` (`douban_id` ASC))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `douban_movies`.`movie_writer`
			-- -----------------------------------------------------
			DROP TABLE IF EXISTS `douban_movies`.`movie_writer` ;

			CREATE TABLE IF NOT EXISTS `douban_movies`.`movie_writer` (
			  `douban_id` INT NOT NULL,
			  `writer_id` INT NOT NULL,
			  PRIMARY KEY (`douban_id`, `writer_id`))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `douban_movies`.`movie_director`
			-- -----------------------------------------------------
			DROP TABLE IF EXISTS `douban_movies`.`movie_director` ;

			CREATE TABLE IF NOT EXISTS `douban_movies`.`movie_director` (
			  `douban_id` INT NOT NULL,
			  `director_id` INT NOT NULL,
			  PRIMARY KEY (`douban_id`, `director_id`))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `douban_movies`.`movie_star`
			-- -----------------------------------------------------
			DROP TABLE IF EXISTS `douban_movies`.`movie_star` ;

			CREATE TABLE IF NOT EXISTS `douban_movies`.`movie_star` (
			  `douban_id` INT NOT NULL,
			  `star_id` INT NOT NULL,
			  PRIMARY KEY (`douban_id`, `star_id`))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `douban_movies`.`movie_genre`
			-- -----------------------------------------------------
			DROP TABLE IF EXISTS `douban_movies`.`movie_genre` ;

			CREATE TABLE IF NOT EXISTS `douban_movies`.`movie_genre` (
			  `douban_id` INT NOT NULL,
			  `genre_id` INT NOT NULL,
			  PRIMARY KEY (`douban_id`, `genre_id`))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `douban_movies`.`movie_location`
			-- -----------------------------------------------------
			DROP TABLE IF EXISTS `douban_movies`.`movie_location` ;

			CREATE TABLE IF NOT EXISTS `douban_movies`.`movie_location` (
			  `douban_id` INT NOT NULL,
			  `location_id` INT NOT NULL,
			  PRIMARY KEY (`douban_id`, `location_id`))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `douban_movies`.`movie_language`
			-- -----------------------------------------------------
			DROP TABLE IF EXISTS `douban_movies`.`movie_language` ;

			CREATE TABLE IF NOT EXISTS `douban_movies`.`movie_language` (
			  `douban_id` INT NOT NULL,
			  `language_id` INT NOT NULL,
			  PRIMARY KEY (`douban_id`, `language_id`))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `douban_movies`.`craw_list`
			-- -----------------------------------------------------
			DROP TABLE IF EXISTS `douban_movies`.`craw_list` ;

			CREATE TABLE IF NOT EXISTS `douban_movies`.`craw_list` (
			  `douban_id` INT NOT NULL,
			  `status` INT NOT NULL,
			  `craw_time` VARCHAR(64) NULL,
			  PRIMARY KEY (`douban_id`),
			  UNIQUE INDEX `douban_id_UNIQUE` (`douban_id` ASC))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `douban_movies`.`tags`
			-- -----------------------------------------------------
			DROP TABLE IF EXISTS `douban_movies`.`tags` ;

			CREATE TABLE IF NOT EXISTS `douban_movies`.`tags` (
			  `tag_id` INT NOT NULL AUTO_INCREMENT,
			  `tag` VARCHAR(128) NULL,
			  PRIMARY KEY (`tag_id`),
			  UNIQUE INDEX `tag_id_UNIQUE` (`tag_id` ASC),
			  UNIQUE INDEX `tag_UNIQUE` (`tag` ASC))
			ENGINE = InnoDB;


			-- -----------------------------------------------------
			-- Table `douban_movies`.`movie_tag`
			-- -----------------------------------------------------
			DROP TABLE IF EXISTS `douban_movies`.`movie_tag` ;

			CREATE TABLE IF NOT EXISTS `douban_movies`.`movie_tag` (
			  `douban_id` INT NOT NULL,
			  `tag_id` INT NOT NULL,
			  PRIMARY KEY (`douban_id`, `tag_id`))
			ENGINE = InnoDB;
		''')

init = TableCreator()
init.create()

print('Created 17 tables successfully.')