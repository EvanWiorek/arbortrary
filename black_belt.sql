-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema arbortrary_schema
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema arbortrary_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `arbortrary_schema` DEFAULT CHARACTER SET utf8 ;
USE `arbortrary_schema` ;

-- -----------------------------------------------------
-- Table `arbortrary_schema`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `arbortrary_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(300) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `arbortrary_schema`.`trees`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `arbortrary_schema`.`trees` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `species` VARCHAR(255) NULL,
  `location` VARCHAR(255) NULL,
  `reason` VARCHAR(55) NULL,
  `date_planted` DATETIME NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
  INDEX `fk_trees_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_trees_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `arbortrary_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `arbortrary_schema`.`page_visits`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `arbortrary_schema`.`page_visits` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `tree_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_visitors_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_visitors_trees1_idx` (`tree_id` ASC) VISIBLE,
  CONSTRAINT `fk_visitors_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `arbortrary_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_visitors_trees1`
    FOREIGN KEY (`tree_id`)
    REFERENCES `arbortrary_schema`.`trees` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
