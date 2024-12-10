-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: wikimap
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `countries`
--

DROP TABLE IF EXISTS `countries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `countries` (
  `name` varchar(255) NOT NULL,
  `population` bigint DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `countries`
--

LOCK TABLES `countries` WRITE;
/*!40000 ALTER TABLE `countries` DISABLE KEYS */;
INSERT INTO `countries` VALUES ('Afghanistan',40218234),('Albania',2837743),('Algeria',44700000),('Andorra',77265),('Angola',32866268),('Argentina',45376763),('Armenia',2963234),('Australia',25687041),('Austria',8917205),('Azerbaijan',10110116),('Bahrain',1701583),('Bangladesh',164689383),('Belarus',9398861),('Belgium',11555997),('Bosnia and Herzegovina',3280815),('Brazil',212559409),('Brunei',437483),('Bulgaria',6927288),('Burkina Faso',20903278),('Burundi',11890781),('Canada',38005238),('Central African Republic',4829764),('Chile',19116209),('China',1402112000),('Colombia',50882884),('Croatia',4047200),('Cuba',11326616),('Curacao',155014),('Cyprus',1207361),('Czechia',10698896),('Denmark',5831404),('Dominican Republic',10847904),('Ecuador',17643060),('Egypt',102334403),('Estonia',1331057),('Eswatini',1160164),('Faroe Islands',48865),('Finland',5530719),('France',67391582),('Georgia',3714000),('Germany',83240525),('Ghana',31072945),('Greece',10715549),('Guatemala',16858333),('Guernsey',62999),('Guinea-Bissau',1967998),('Hungary',9749763),('Iceland',366425),('India',1380004385),('Indonesia',273523621),('Iran',83992953),('Iraq',40222503),('Ireland',4994724),('Isle of Man',85032),('Israel',9216900),('Italy',59554023),('Jamaica',2961161),('Japan',125836021),('Jersey',100800),('Jordan',10203140),('Kenya',53771300),('Kuwait',4270563),('Kyrgyzstan',6591600),('Latvia',1901548),('Lebanon',6825442),('Libya',6871287),('Liechtenstein',38137),('Lithuania',2794700),('Luxembourg',632275),('Malawi',19129955),('Malaysia',32365998),('Malta',525285),('Marshall Islands',59194),('Mauritius',1265740),('Mexico',128932753),('Moldova',2617820),('Monaco',39244),('Montenegro',621718),('Morocco',36910558),('Nauru',10834),('Netherlands',16655799),('New Zealand',5084300),('Nigeria',206139587),('North Korea',25778815),('North Macedonia',2077132),('Northern Cyprus',NULL),('Norway',5379475),('Pakistan',220892331),('Palestinian Territory',NULL),('Panama',4314768),('Paraguay',7132530),('Peru',32971846),('Philippines',109581085),('Poland',37950802),('Portugal',10305564),('Romania',19286123),('Russia',144104080),('Saudi Arabia',34813867),('Serbia',6908224),('Slovakia',5458827),('Slovenia',2100126),('South Africa',59308690),('South Korea',51780579),('Spain',47351567),('Sri Lanka',21919000),('Sudan',43849269),('Sweden',10353442),('Switzerland',8654622),('Syria',17500657),('Taiwan',23503349),('Tajikistan',9537642),('Tanzania',59734213),('Trinidad and Tobago',1399491),('Tunisia',11818618),('Turkey',84339067),('Uganda',45741000),('Ukraine',44134693),('United Kingdom',67215293),('United States',329484123),('Uruguay',3473727),('Uzbekistan',34232050),('Venezuela',28435943),('Vietnam',97338583),('Zimbabwe',14862927);
/*!40000 ALTER TABLE `countries` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-10 22:25:31
