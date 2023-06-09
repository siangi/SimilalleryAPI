CREATE DATABASE  IF NOT EXISTS `scheme_test_similallery` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `scheme_test_similallery`;
-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: scheme_test_similallery
-- ------------------------------------------------------
-- Server version	8.0.32

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

--
-- Table structure for table `nationality`
--

DROP TABLE IF EXISTS `nationality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nationality` (
  `idnationality` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`idnationality`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nationality`
--

LOCK TABLES `nationality` WRITE;
/*!40000 ALTER TABLE `nationality` DISABLE KEYS */;
INSERT INTO `nationality` VALUES (7,''),(51,'1799-1865'),(62,'1849–1918'),(75,'active 1695-1700 in Amsterdam'),(17,'Afghan'),(8,'American'),(49,'Argentine'),(46,'Argentinian'),(59,'Armenian'),(30,'Australian'),(6,'Austrian'),(60,'Belarusian'),(33,'Belgian'),(67,'Bolivian'),(58,'Bosnian'),(42,'Brazilian'),(83,'Bulgarian'),(40,'Canadian'),(81,'Chilean'),(56,'Chinese'),(54,'Cirlce'),(74,'Colombian'),(41,'Croatian'),(82,'Cuban'),(19,'Czech'),(72,'D. Th'),(28,'Danish'),(9,'Dutch'),(80,'Ecuadorian'),(11,'English'),(38,'Estonian'),(29,'Finnish'),(26,'Flemish'),(13,'French'),(43,'Georgian'),(15,'German'),(36,'Greek'),(18,'Hungarian'),(57,'Indian'),(64,'Indonesian'),(70,'Iranian'),(65,'Iraqi'),(32,'Irish'),(21,'Italian'),(37,'Japanese'),(55,'Latvian'),(69,'Lebanese'),(73,'Lithuanian'),(27,'Maltese'),(45,'Mexican'),(53,'New Zealander'),(76,'Northern European'),(16,'Norwegian'),(25,'Peruvian'),(10,'Polish'),(39,'Portuguese'),(77,'Possibly Benedetto Caliari'),(47,'Romanian'),(14,'Russian'),(24,'Scottish'),(61,'Serbian'),(34,'Slovak'),(48,'Slovenian'),(44,'South African'),(66,'South Korean'),(23,'Spanish'),(78,'Sri Lankan'),(63,'Studio'),(20,'Swedish'),(12,'Swiss'),(71,'Trinidadian'),(35,'Turkish'),(22,'Ukrainian'),(50,'Uruguayan'),(68,'Venezuelan'),(31,'Welsh'),(79,'Workshop'),(52,'Yugoslavian');
/*!40000 ALTER TABLE `nationality` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-09 12:04:38
