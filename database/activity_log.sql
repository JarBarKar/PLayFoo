-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 14, 2019 at 06:42 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `room`
--
CREATE DATABASE IF NOT EXISTS `activity_log` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `activity_log`;

-- --------------------------------------------------------

--
-- Table structure for table `room`
--

DROP TABLE IF EXISTS `activity_log`;
CREATE TABLE IF NOT EXISTS `activity_log` (
  `activity_id` int(6) NOT NULL AUTO_INCREMENT,
  `code` int(3) NOT NULL,
  `data` varchar(1000) NOT NULL,
  `message` varchar(128) NOT NULL,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`activity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `room`
--

INSERT INTO `activity_log` (`activity_id`, `code`, `data`,`message`, `timestamp`) VALUES
(1, 200 ,'123123','Joined a Room',  CURRENT_TIMESTAMP()),
(2, 502, 'testgay', 'Failed room joining. Damn!', CURRENT_TIMESTAMP());
COMMIT;

