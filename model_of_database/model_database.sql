CREATE DATABASE IF NOT EXISTS `kompas` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `kompas`;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id`                int          NOT NULL AUTO_INCREMENT,
  `first_name`        varchar(100) NOT NULL,
  `last_name`         varchar(100) NOT NULL,
  `username`          varchar(100) NOT NULL,
  `email`             varchar(150) NOT NULL,
  `password`          varchar(255) NOT NULL,
  `contact`           varchar(50)  DEFAULT NULL,
  `status`            enum('active','pending') DEFAULT 'pending',
  `role`              enum('user','admin')    DEFAULT 'user',
  `registered_at`     datetime     DEFAULT CURRENT_TIMESTAMP,
  `rejection_reason`  text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email`    (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `company`;
CREATE TABLE `company` (
  `id`               int          NOT NULL AUTO_INCREMENT,
  `name`             varchar(150) NOT NULL,
  `username`         varchar(100) NOT NULL,
  `email`            varchar(150) DEFAULT NULL,
  `password`         varchar(255) DEFAULT NULL,
  `industry`         varchar(150) DEFAULT NULL,
  `contact`          varchar(150) DEFAULT NULL,
  `description`      text,
  `logo_path`        varchar(500) DEFAULT NULL,
  `status`           enum('active','pending') DEFAULT 'pending',
  `rejection_reason` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email`    (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `administrator`;
CREATE TABLE `administrator` (
  `id`            int  NOT NULL AUTO_INCREMENT,
  `user_id`       int  NOT NULL,
  `access_level`  varchar(50) DEFAULT NULL,
  `assigned_date` date        DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `administrator_user_fk` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `skill`;
CREATE TABLE `skill` (
  `id`          int          NOT NULL AUTO_INCREMENT,
  `name`        varchar(100) NOT NULL,
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `career`;
CREATE TABLE `career` (
  `id`          int          NOT NULL AUTO_INCREMENT,
  `name`        varchar(150) NOT NULL,
  `description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `career_skill`;
CREATE TABLE `career_skill` (
  `career_id`      int            NOT NULL,
  `skill_id`       int            NOT NULL,
  `required_level` int            NOT NULL,
  `weight`         decimal(3,2)   DEFAULT '1.00',
  PRIMARY KEY (`career_id`, `skill_id`),
  KEY `skill_id` (`skill_id`),
  CONSTRAINT `career_skill_career_fk` FOREIGN KEY (`career_id`) REFERENCES `career` (`id`) ON DELETE CASCADE,
  CONSTRAINT `career_skill_skill_fk`  FOREIGN KEY (`skill_id`)  REFERENCES `skill`  (`id`) ON DELETE CASCADE,
  CONSTRAINT `career_skill_level_chk` CHECK (`required_level` BETWEEN 1 AND 5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `user_skill`;
CREATE TABLE `user_skill` (
  `user_id`  int NOT NULL,
  `skill_id` int NOT NULL,
  `level`    int NOT NULL,
  PRIMARY KEY (`user_id`, `skill_id`),
  KEY `skill_id` (`skill_id`),
  CONSTRAINT `user_skill_user_fk`  FOREIGN KEY (`user_id`)  REFERENCES `user`  (`id`) ON DELETE CASCADE,
  CONSTRAINT `user_skill_skill_fk` FOREIGN KEY (`skill_id`) REFERENCES `skill` (`id`) ON DELETE CASCADE,
  CONSTRAINT `user_skill_level_chk` CHECK (`level` BETWEEN 1 AND 5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `resource`;
CREATE TABLE `resource` (
  `id`          int          NOT NULL AUTO_INCREMENT,
  `skill_id`    int          NOT NULL,
  `name`        varchar(255) NOT NULL,
  `url`         varchar(500) DEFAULT NULL,
  `level`       varchar(50)  DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `skill_id` (`skill_id`),
  CONSTRAINT `resource_skill_fk` FOREIGN KEY (`skill_id`) REFERENCES `skill` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `career_project`;
CREATE TABLE `career_project` (
  `id`          int          NOT NULL AUTO_INCREMENT,
  `career_id`   int          NOT NULL,
  `name`        varchar(255) NOT NULL,
  `description` text,
  `level`       varchar(100) DEFAULT NULL,
  `file_path`   varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `career_id` (`career_id`),
  CONSTRAINT `career_project_career_fk` FOREIGN KEY (`career_id`) REFERENCES `career` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `job_ad`;
CREATE TABLE `job_ad` (
  `id`                   int          NOT NULL AUTO_INCREMENT,
  `company_id`           int          NOT NULL,
  `name`                 varchar(150) NOT NULL,
  `description`          text,
  `type`                 enum('internship','junior') NOT NULL,
  `location`             varchar(150) DEFAULT NULL,
  `application_deadline` date         DEFAULT NULL,
  `created_at`           datetime     DEFAULT CURRENT_TIMESTAMP,
  `updated_at`           datetime     DEFAULT NULL,
  `status`               enum('active','inactive','pending') DEFAULT 'pending',
  `removal_reason`       text,
  PRIMARY KEY (`id`),
  KEY `company_id` (`company_id`),
  CONSTRAINT `job_ad_company_fk` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `job_ad_skill`;
CREATE TABLE `job_ad_skill` (
  `job_ad_id`      int NOT NULL,
  `skill_id`       int NOT NULL,
  `required_level` int NOT NULL,
  PRIMARY KEY (`job_ad_id`, `skill_id`),
  KEY `skill_id` (`skill_id`),
  CONSTRAINT `job_ad_skill_job_ad_fk` FOREIGN KEY (`job_ad_id`) REFERENCES `job_ad` (`id`) ON DELETE CASCADE,
  CONSTRAINT `job_ad_skill_skill_fk`  FOREIGN KEY (`skill_id`)  REFERENCES `skill`  (`id`) ON DELETE CASCADE,
  CONSTRAINT `job_ad_skill_level_chk` CHECK (`required_level` BETWEEN 1 AND 5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `application`;
CREATE TABLE `application` (
  `id`         int      NOT NULL AUTO_INCREMENT,
  `user_id`    int      NOT NULL,
  `job_ad_id`  int      NOT NULL,
  `applied_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status`     enum('active','withdrawn') NOT NULL DEFAULT 'active',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_job_ad` (`user_id`, `job_ad_id`),
  KEY `job_ad_id` (`job_ad_id`),
  CONSTRAINT `application_user_fk`   FOREIGN KEY (`user_id`)   REFERENCES `user`   (`id`) ON DELETE CASCADE,
  CONSTRAINT `application_job_ad_fk` FOREIGN KEY (`job_ad_id`) REFERENCES `job_ad` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `subscription`;
CREATE TABLE `subscription` (
  `id`         int          NOT NULL AUTO_INCREMENT,
  `user_id`    int          DEFAULT NULL,
  `company_id` int          DEFAULT NULL,
  `amount`     decimal(8,2) NOT NULL DEFAULT '10.00',
  `status`     enum('success','failed','cancelled') NOT NULL,
  `date`       datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id`    (`user_id`),
  KEY `company_id` (`company_id`),
  CONSTRAINT `subscription_user_fk`    FOREIGN KEY (`user_id`)    REFERENCES `user`    (`id`) ON DELETE SET NULL,
  CONSTRAINT `subscription_company_fk` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `password_reset`;
CREATE TABLE `password_reset` (
  `id`         int          NOT NULL AUTO_INCREMENT,
  `user_id`    int          DEFAULT NULL,
  `company_id` int          DEFAULT NULL,
  `token`      varchar(255) NOT NULL,
  `expires_at` datetime     NOT NULL,
  `is_used`    tinyint(1)   DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  KEY `user_id`    (`user_id`),
  KEY `company_id` (`company_id`),
  CONSTRAINT `password_reset_user_fk`    FOREIGN KEY (`user_id`)    REFERENCES `user`    (`id`) ON DELETE CASCADE,
  CONSTRAINT `password_reset_company_fk` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `favorite_career`;
CREATE TABLE `favorite_career` (
  `user_id`   int NOT NULL,
  `career_id` int NOT NULL,
  PRIMARY KEY (`user_id`, `career_id`),
  KEY `career_id` (`career_id`),
  CONSTRAINT `favorite_career_user_fk`   FOREIGN KEY (`user_id`)   REFERENCES `user`   (`id`) ON DELETE CASCADE,
  CONSTRAINT `favorite_career_career_fk` FOREIGN KEY (`career_id`) REFERENCES `career` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `favorite_job_ad`;
CREATE TABLE `favorite_job_ad` (
  `user_id`   int NOT NULL,
  `job_ad_id` int NOT NULL,
  PRIMARY KEY (`user_id`, `job_ad_id`),
  KEY `job_ad_id` (`job_ad_id`),
  CONSTRAINT `favorite_job_ad_user_fk`   FOREIGN KEY (`user_id`)   REFERENCES `user`   (`id`) ON DELETE CASCADE,
  CONSTRAINT `favorite_job_ad_job_ad_fk` FOREIGN KEY (`job_ad_id`) REFERENCES `job_ad` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `favorite_candidate`;
CREATE TABLE `favorite_candidate` (
  `company_id` int NOT NULL,
  `user_id`    int NOT NULL,
  `job_ad_id`  int NOT NULL,
  PRIMARY KEY (`company_id`, `user_id`, `job_ad_id`),
  KEY `user_id`   (`user_id`),
  KEY `job_ad_id` (`job_ad_id`),
  CONSTRAINT `favorite_candidate_company_fk` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`) ON DELETE CASCADE,
  CONSTRAINT `favorite_candidate_user_fk`    FOREIGN KEY (`user_id`)    REFERENCES `user`    (`id`) ON DELETE CASCADE,
  CONSTRAINT `favorite_candidate_job_ad_fk`  FOREIGN KEY (`job_ad_id`)  REFERENCES `job_ad`  (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;