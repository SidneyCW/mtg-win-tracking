/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.5.26-MariaDB, for debian-linux-gnueabihf (armv8l)
--
-- Host: localhost    Database: mtg_tracker
-- ------------------------------------------------------
-- Server version	10.5.26-MariaDB-0+deb11u2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `match_players`
--

DROP TABLE IF EXISTS `match_players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `match_players` (
  `match_id` int(11) DEFAULT NULL,
  `player_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `deck` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  KEY `match_id` (`match_id`),
  CONSTRAINT `match_players_ibfk_1` FOREIGN KEY (`match_id`) REFERENCES `matches` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `match_players`
--

LOCK TABLES `match_players` WRITE;
/*!40000 ALTER TABLE `match_players` DISABLE KEYS */;
INSERT INTO `match_players` VALUES (1,'Sidney','Eldrazi'),(1,'Jack','ManaBurn'),(1,'Cole','Dragon'),(2,'Alice','Life Gain'),(2,'Alex A','Blue'),(2,'Cameron','Green White'),(2,'Jack A','Red Blue'),(3,'Jack','Assassin'),(3,'Alice','Life Gain'),(3,'Sidney','Ninja'),(3,'Alex A','Theft'),(4,'Jack A','Krenko'),(4,'Cole','Dragon'),(4,'Cameron','Green White'),(4,'Priscilla','Red Green'),(5,'Jack A','Red Blue'),(5,'Alice','Blue'),(5,'Sidney','Red Green'),(5,'Cameron','Green White'),(6,'Cole','Mardu'),(6,'Keean','white black'),(6,'Jack','Assassin'),(6,'Sidney','Mardu'),(6,'Romeo','Vehicle'),(7,'Vince','Eldrazi'),(7,'Keean','Red Green'),(7,'Romeo','Vehicle'),(7,'Jack','ManaBurn'),(7,'Sidney','Red Green'),(8,'Jack','Krenko'),(8,'Romeo','White Green'),(8,'Cole','Miku'),(8,'Keean','white black'),(8,'Sidney','Ninja'),(9,'Cole','Dragon'),(9,'Keean','Sliver'),(9,'Romeo','Legendary'),(9,'Sidney','Eldrazi'),(9,'Jack','Assassin'),(10,'Vince','Eldrazi'),(10,'Cole','Dragon'),(10,'Keean','Rat'),(10,'Jack','Vraska'),(10,'Sidney','Ninja'),(11,'Keean','Artifact'),(11,'Jack','ManaBurn'),(11,'Vince','Eldrazi'),(11,'Cole','Dragon'),(11,'Sidney','Ninja'),(12,'Alice','Red Green'),(12,'Lucky','Assassin'),(12,'Cole','Eldrazi'),(12,'Sidney','Ninja'),(12,'Jack','Jeskai'),(13,'Jack','Jeskai'),(13,'Cole','Eldrazi'),(13,'Alice','Red Green'),(14,'Jack','Jeskai'),(14,'Cole','Eldrazi'),(14,'Alice','Red Green'),(15,'Jack','Jeskai'),(15,'Sidney','Eldrazi'),(15,'Lucky','Assassin'),(16,'Cole','Eldrazi'),(16,'Sidney','Eldrazi'),(16,'Vince','Ninja'),(16,'Josh','Cat'),(16,'Jack','Jeskai'),(17,'Vince','Kaching Eldrazi'),(17,'Cole','Dragon'),(17,'Khang','Cat'),(17,'Sidney','Ninja'),(18,'Khang','Eldrazi'),(18,'Cole','Dragon'),(18,'Vince','Kaching Eldrazi'),(18,'Sidney','Ninja'),(19,'Jack','Jeskai'),(19,'Cole','Eldrazi'),(19,'Sidney','Ninja');
/*!40000 ALTER TABLE `match_players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `matches`
--

DROP TABLE IF EXISTS `matches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `matches` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `match_key` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `winner` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `play_num` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `match_key` (`match_key`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matches`
--

LOCK TABLES `matches` WRITE;
/*!40000 ALTER TABLE `matches` DISABLE KEYS */;
INSERT INTO `matches` VALUES (1,'1SJC','Jack',3),(2,'2AACJ','Alice',4),(3,'3JASA','Jack',4),(4,'4JCCP','Cole',4),(5,'5JASC','Jack A',4),(6,'6CKJSR','Cole',5),(7,'7VKRJS','Jack',5),(8,'8JRCKS','Romeo',5),(9,'9CKRSJ','Sidney',5),(10,'10VCKJS','Jack',5),(11,'11KJVCS','Keean',5),(12,'12ALCSJ','Lucky',5),(13,'13JCA','Jack',3),(14,'14JCA','Jack',3),(15,'15JSL','Jack',3),(16,'16CSVJJ','Cole',5),(17,'17VCKS','Vince',4),(18,'18KCVS','Cole',4),(19,'19JCS','Jack',3);
/*!40000 ALTER TABLE `matches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `player_decks`
--

DROP TABLE IF EXISTS `player_decks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `player_decks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `player_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `deck` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `wins` int(11) DEFAULT 0,
  `games_played` int(11) DEFAULT 0,
  `elo` int(11) DEFAULT 1000,
  PRIMARY KEY (`id`),
  UNIQUE KEY `player_name` (`player_name`,`deck`),
  CONSTRAINT `player_decks_ibfk_1` FOREIGN KEY (`player_name`) REFERENCES `users` (`name`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `player_decks`
--

LOCK TABLES `player_decks` WRITE;
/*!40000 ALTER TABLE `player_decks` DISABLE KEYS */;
INSERT INTO `player_decks` VALUES (1,'Sidney','Eldrazi',1,4,1000),(2,'Jack','ManaBurn',2,3,1000),(3,'Cole','Dragon',2,7,1000),(4,'Alice','Life Gain',1,2,1000),(5,'Alex A','Blue',0,1,1000),(6,'Cameron','Green White',0,3,1000),(7,'Jack A','Red Blue',1,2,1000),(8,'Jack','Assassin',1,3,1000),(9,'Sidney','Ninja',0,8,1000),(10,'Alex A','Theft',0,1,1000),(11,'Jack A','Krenko',0,1,1000),(12,'Priscilla','Red Green',0,1,1000),(13,'Alice','Blue',0,1,1000),(14,'Sidney','Red Green',0,2,1000),(15,'Vince','Black',0,0,1000),(16,'Keean','white black',0,2,1000),(17,'Cole','Mardu',1,1,1000),(18,'Sidney','Mardu',0,1,1000),(19,'Romeo','Vehicle',0,2,1000),(20,'Sidney','Cat',0,0,1000),(21,'Alice','Monoblue',0,0,1000),(22,'Vince','Eldrazi',0,3,1000),(23,'Keean','Red Green',0,1,1000),(24,'Keean','Black White',0,0,1000),(25,'Cole','Miku',0,1,1000),(26,'Romeo','White Green',1,1,1000),(27,'Jack','Krenko',0,1,1000),(28,'Keean','Sliver',0,1,1000),(29,'Romeo','Legendary',0,1,1000),(30,'Jack','Vraska',1,1,1000),(31,'Keean','Rat',0,1,1000),(32,'Keean','Artifact',1,1,1000),(33,'Lucky','Assassin',1,2,1000),(34,'Jack','Jeskai',4,6,1000),(35,'Cole','Eldrazi',1,5,1000),(36,'Alice','Red Green',0,3,1000),(37,'Josh','Cat',0,1,1000),(38,'Vince','Ninja',0,1,1000),(39,'Vince','Kaching Eldrazi',1,2,1000),(40,'Khang','Cat',0,1,1000),(41,'Khang','Eldrazi',0,1,1000);
/*!40000 ALTER TABLE `player_decks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `wins` int(11) DEFAULT 0,
  `losses` int(11) DEFAULT 0,
  `elo` int(11) DEFAULT 1000,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Sidney',1,14,1000),(2,'Jack',8,6,1000),(3,'Cole',4,10,1000),(4,'Alice',1,5,1000),(5,'Alex A',0,2,1000),(6,'Cameron',0,3,1000),(7,'Jack A',1,2,1000),(8,'Priscilla',0,1,1000),(9,'Vince',1,5,1000),(10,'Keean',1,5,1000),(11,'Romeo',1,3,1000),(12,'Lucky',1,1,1000),(13,'Josh',0,1,1000),(14,'Khang',0,2,1000);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-06  1:53:56
