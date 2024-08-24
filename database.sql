-- MySQL dump 10.19  Distrib 10.3.39-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: db_escuela
-- ------------------------------------------------------
-- Server version	10.3.39-MariaDB-0ubuntu0.20.04.2

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
-- Table structure for table `tb_credenciales`
--

DROP TABLE IF EXISTS `tb_credenciales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_credenciales` (
  `id_credencial` int(11) NOT NULL AUTO_INCREMENT,
  `id_username` varchar(50) NOT NULL,
  `password` text DEFAULT NULL,
  `position` varchar(50) NOT NULL,
  `fk_user_id` varchar(50) NOT NULL,
  PRIMARY KEY (`id_credencial`),
  KEY `fk_user_id_constraint` (`fk_user_id`),
  CONSTRAINT `fk_user_id_constraint` FOREIGN KEY (`fk_user_id`) REFERENCES `tb_users` (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_credenciales`
--

LOCK TABLES `tb_credenciales` WRITE;
/*!40000 ALTER TABLE `tb_credenciales` DISABLE KEYS */;
INSERT INTO `tb_credenciales` VALUES (2,'admin','pbkdf2:sha256:150000$7lrdWEFd$937b27375ef555fdef2a34cd1757b83855f528fa35d7865611a10bac2865e080','administrador','V-31387119');
/*!40000 ALTER TABLE `tb_credenciales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_email_blocking`
--

DROP TABLE IF EXISTS `tb_email_blocking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_email_blocking` (
  `id_lock` int(11) NOT NULL AUTO_INCREMENT,
  `id_user_lock` varchar(50) NOT NULL,
  `attempts` int(11) NOT NULL,
  `blocking_time` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_lock`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_email_blocking`
--

LOCK TABLES `tb_email_blocking` WRITE;
/*!40000 ALTER TABLE `tb_email_blocking` DISABLE KEYS */;
INSERT INTO `tb_email_blocking` VALUES (1,'v-31387119',0,'2024-08-13 23:52:53.555375');
/*!40000 ALTER TABLE `tb_email_blocking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_sections`
--

DROP TABLE IF EXISTS `tb_sections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_sections` (
  `id_section` varchar(20) NOT NULL,
  `storage` int(50) NOT NULL,
  `classroom` varchar(100) NOT NULL,
  `fk_teacher_id` varchar(50) NOT NULL,
  PRIMARY KEY (`id_section`),
  KEY `tk_teacher_id` (`fk_teacher_id`),
  CONSTRAINT `tb_sections_ibfk_1` FOREIGN KEY (`fk_teacher_id`) REFERENCES `tb_users` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_sections`
--

LOCK TABLES `tb_sections` WRITE;
/*!40000 ALTER TABLE `tb_sections` DISABLE KEYS */;
INSERT INTO `tb_sections` VALUES ('1A',30,'aula 01','V-31387119');
/*!40000 ALTER TABLE `tb_sections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_students`
--

DROP TABLE IF EXISTS `tb_students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_students` (
  `id_student` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `surname` varchar(50) NOT NULL,
  `birthdate` date NOT NULL,
  `fk_id_representante` varchar(50) NOT NULL,
  `fk_id_section` varchar(50) NOT NULL,
  PRIMARY KEY (`id_student`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_students`
--

LOCK TABLES `tb_students` WRITE;
/*!40000 ALTER TABLE `tb_students` DISABLE KEYS */;
INSERT INTO `tb_students` VALUES ('1234','Luis Adrian','Colemanres Antolinez','2024-01-01','V-14984561','1A'),('2020','Abrahan jose','Colmenares antolinez','2024-01-01','V-14984561','1A'),('2021','yonkleibessor alexander','Colmenares antolinez','2024-01-01','V-14984561','1A');
/*!40000 ALTER TABLE `tb_students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_users`
--

DROP TABLE IF EXISTS `tb_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_users` (
  `id_user` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `surname` varchar(50) NOT NULL,
  `birthdate` date NOT NULL,
  `phone` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `address` varchar(50) NOT NULL,
  `profile_picture` varchar(100) NOT NULL,
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_users`
--

LOCK TABLES `tb_users` WRITE;
/*!40000 ALTER TABLE `tb_users` DISABLE KEYS */;
INSERT INTO `tb_users` VALUES ('V-31387119','Abrahan','Colmenares','2024-01-01','+58 414-7359478','abrahancolmenares022@gmail.com','ninguno','1723509469422.png');
/*!40000 ALTER TABLE `tb_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-24 16:09:02
