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
-- Database: `message`
--
CREATE DATABASE IF NOT EXISTS `message` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `message`;

-- --------------------------------------------------------

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
CREATE TABLE IF NOT EXISTS `message` (
  `message_id` int(6) NOT NULL AUTO_INCREMENT,
  `room_id` int(6) NOT NULL,
  `user_id` varchar(12) NOT NULL,
  `content` varchar(150) NOT NULL,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`message_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `message`
--

INSERT INTO `message` (`message_id`, `room_id`, `user_id`, `content`, `timestamp`) VALUES
(1,1, 'edwinlzs', 'first message everrrrr',CURRENT_TIMESTAMP()),
(2,2, 'weeasdb', 'second message everrrrr',CURRENT_TIMESTAMP()),
(3,2, 'weeewrgb', 'muda',CURRENT_TIMESTAMP()),
(4,2, 'weejb', 'zawado',CURRENT_TIMESTAMP()),
(5,2, 'weebng', 'mistaaaa',CURRENT_TIMESTAMP()),
(6,2, 'weaeb', 'booby',CURRENT_TIMESTAMP());
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
