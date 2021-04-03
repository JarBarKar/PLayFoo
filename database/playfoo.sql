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
-- Database: `playfoo`
--
CREATE DATABASE IF NOT EXISTS `playfoo` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `playfoo`;

-- --------------------------------------------------------

--
-- Table structure for table `room`
--

DROP TABLE IF EXISTS `room`;
CREATE TABLE IF NOT EXISTS `room` (
  `room_id` int(6) NOT NULL AUTO_INCREMENT,
  `room_name` varchar(64) NOT NULL,
  `game_id` int(3) NOT NULL,
  `capacity` int(2) NOT NULL,
  `host_id` varchar(12) NOT NULL,
  PRIMARY KEY (`room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `room`
--

INSERT INTO `room` (`room_id`, `room_name`, `game_id`, `capacity`, `host_id`) VALUES
(1, 'First room everrrr', 265, 24, 'edwinlzs'),
(2, 'Second room everrrr', 10, 2, 'weeb');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- --------------------------------------------------------

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
CREATE TABLE IF NOT EXISTS `member` (
  `room_id` int(6) NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`room_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `member`
--

INSERT INTO `member` (`room_id`, `user_id`) VALUES
(1, 'edwinlzs'),
(1, 'sugarbaby'),
(2, 'weeb'),
(2, 'test'),
(2, 'aaron');
COMMIT;

-- --------------------------------------------------------

--
-- Table structure for table `activity_log`
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
-- Dumping data for table `activity_log`
--

INSERT INTO `activity_log` (`activity_id`, `code`, `data`,`message`, `timestamp`) VALUES
(1, 200 ,'123123','Joined a Room',  CURRENT_TIMESTAMP()),
(2, 502, 'testgay', 'Failed room joining. Damn!', CURRENT_TIMESTAMP());
COMMIT;

-- --------------------------------------------------------

--
-- Table structure for table `error`
--

DROP TABLE IF EXISTS `error`;
CREATE TABLE IF NOT EXISTS `error` (
  `error_id` int(6) NOT NULL AUTO_INCREMENT,
  `code` int(3) NOT NULL,
  `data` varchar(1000) NOT NULL,
  `message` varchar(128) NOT NULL,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`error_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `error`
--

INSERT INTO `error` (`error_id`, `code`, `data`,`message`, `timestamp`) VALUES
(1, 200 ,'123123','Joined a Room',  CURRENT_TIMESTAMP()),
(2, 502, 'testgay', 'Failed room joining. Damn!', CURRENT_TIMESTAMP());
COMMIT;

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
  PRIMARY KEY (`message_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `message`
--

INSERT INTO `message` (`message_id`, `room_id`, `user_id`, `content`) VALUES
(1, 1, 'edwinlzs', 'first message everrrrr'),
(2, 2, 'weeb', 'second message everrrrr');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

--
-- Database: `user`
--
CREATE DATABASE IF NOT EXISTS `user` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user`;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` varchar(12) NOT NULL,
  `password` varchar(16) NOT NULL,
  `token` varchar(100) NOT NULL
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `password`, `token`) VALUES
('edwinlzs', 'Edwin','edwinlzsEdwin'),
('weeb', 'Onii-San','weebOnii-San'),
('test', 'Tester','testTester');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;