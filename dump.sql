-- MySQL dump 10.13  Distrib 8.0.17, for Win64 (x86_64)
--
-- Host: localhost    Database: tgbot
-- ------------------------------------------------------
-- Server version	8.0.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `id` varchar(20) DEFAULT NULL,
  `password` varchar(28) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES ('Nick','1');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grades`
--

DROP TABLE IF EXISTS `grades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grades` (
  `school_id` varchar(4) DEFAULT NULL,
  `number_grade` varchar(8) DEFAULT NULL,
  `grade_id` varchar(4) DEFAULT NULL,
  `photo_teacher` varchar(128) DEFAULT NULL,
  `name_of_teacher` varchar(64) DEFAULT NULL,
  `invite_url` bigint(20) DEFAULT NULL,
  `bulletin_board` varchar(1024) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grades`
--

LOCK TABLES `grades` WRITE;
/*!40000 ALTER TABLE `grades` DISABLE KEYS */;
INSERT INTO `grades` VALUES ('001','10а','001','img\\учитель.jpg','Ольгя Валентиновка Парасяк',1,'Доска объявлений, тестовая.'),('001','11а','002','img\\учитель.jpg','Биляшка Ольга',1,'Доска объявлений, тестовая. Для другого класса.'),('002','7а','001','img\\учитель.jpg','Тестовый',-1001347602161,'Доска объявлений, тестовая.'),('002','8а','002','img\\учитель.jpg','Тестовый',-1001347602161,'Доска объявлений, тестовая.'),('001','4а','003','C:\\PyProj\\schoolbot\\img\\Вторая Пикча — копия.png','Это уже тестил',-1,'Кексики по доллар.Всем ку, я баку.\n\n\nВторая запись\n\n\n'),('123','12398','001','Новый класс','Новый класс',-1,'Новый класс'),('123','9','002','C:\\PyProj\\schoolbot\\img\\Первая Пикча.png','Кексик',-1,'Новый классфывфывфыв\n\n\n\n\n\nkeks'),('123','1б','003','C:\\PyProj\\schoolbot\\img\\учитель.jpg','Кекс',-1,'Новый классВведеная инфа)\n\n\n'),('101','10а','001','C:\\PyProj\\schoolbot\\img\\учитель.jpg','Новый препод',-1,'Новый класс'),('101','11а','002','C:\\PyProj\\schoolbot\\img\\учитель.jpg','Бабло',123123123,'Новый классфывфыв\n\n\n');
/*!40000 ALTER TABLE `grades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `homework`
--

DROP TABLE IF EXISTS `homework`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `homework` (
  `school_id` varchar(4) DEFAULT NULL,
  `grade_id` varchar(4) DEFAULT NULL,
  `subject` varchar(16) DEFAULT NULL,
  `homework` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `homework`
--

LOCK TABLES `homework` WRITE;
/*!40000 ALTER TABLE `homework` DISABLE KEYS */;
INSERT INTO `homework` VALUES ('001','001','русский','asd'),('002','001','математика','hello'),('001','002','русский','asd'),('001','001','Физика','Номер 5'),('001','001','математика','номер 343'),('001','003','русский','Новое дз'),('002','001','физика','фыв');
/*!40000 ALTER TABLE `homework` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marks`
--

DROP TABLE IF EXISTS `marks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `marks` (
  `school_id` varchar(4) DEFAULT NULL,
  `grade_id` varchar(4) DEFAULT NULL,
  `stud_id` varchar(4) DEFAULT NULL,
  `name_of_subject` varchar(16) DEFAULT NULL,
  `mark` varchar(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marks`
--

LOCK TABLES `marks` WRITE;
/*!40000 ALTER TABLE `marks` DISABLE KEYS */;
INSERT INTO `marks` VALUES ('001','001','123','русский','4'),('001','001','123','русский','4'),('001','001','123','математика','5'),('001','001','123','математика','2'),('001','001','123','русский','2'),('001','001','002','русский','3'),('001','001','002','русский','2'),('001','001','002','русский','6'),('001','003','123','русский','3'),('001','003','1','русский','5'),('001','003','123','русский','5'),('001','001','123','русский','5'),('001','001','123','русский','5'),('001','001','002','русский','5'),('002','001','002','физика','5'),('002','001','002','физика','3');
/*!40000 ALTER TABLE `marks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `res`
--

DROP TABLE IF EXISTS `res`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `res` (
  `name` varchar(32) DEFAULT NULL,
  `value` varchar(1024) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `res`
--

LOCK TABLES `res` WRITE;
/*!40000 ALTER TABLE `res` DISABLE KEYS */;
INSERT INTO `res` VALUES ('картинка1','C:\\PyProj\\schoolbot\\img\\Первая Пикча.png'),('реклама1','Новая реклама'),('картинка2','C:\\PyProj\\schoolbot\\img\\Вторая Пикча.png'),('реклама2','Вторая реклама');
/*!40000 ALTER TABLE `res` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schools`
--

DROP TABLE IF EXISTS `schools`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schools` (
  `name_school` varchar(64) DEFAULT NULL,
  `slogan` varchar(64) DEFAULT NULL,
  `school_id` varchar(8) DEFAULT NULL,
  `news_of_school` varchar(512) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schools`
--

LOCK TABLES `schools` WRITE;
/*!40000 ALTER TABLE `schools` DISABLE KEYS */;
INSERT INTO `schools` VALUES ('Первое новое название школы 001;','Всем здрасти, забор покрасьти.','001','ШОК! Собака съела шарик.\n\n\nПервоклашки поступили в первый класс!\n\n\nВозле 9-а случился пожар! Бегите все!!!\n\n\n'),('ОШ 1234','Мы - топ школа!','002','ШОК! Собака съела шарик.\n\n\nПервоклашки поступили в первый класс!\n\n\n'),('Тестовая школа','Мы лучшие!!!','003','Завтра род. собрание на 9.'),('Вторая тест школа','Новосозданная школа','004','asd'),('Кексик','Крутой текст','005','Крутая афиша'),('Нормальное название школы','Новосозданная школа','123','АфишаНовая афиша\n\n\n\n\n\nНовая афиша'),('Новая шк','Новосозданная школа','101','Сегодня понедельник, ура!!!');
/*!40000 ALTER TABLE `schools` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `school_id` varchar(4) DEFAULT NULL,
  `grade_id` varchar(4) DEFAULT NULL,
  `name` varchar(32) DEFAULT NULL,
  `stud_id` varchar(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES ('001','001','Никита Куркурин','123'),('001','001','Сергей Иорданов','002'),('002','001','Коля','002'),('001','003','Николай','123'),('001','003','Николай Смирнов','1'),('123','003','Сашка','001'),('101','002','Степка','002');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers` (
  `school_id` varchar(4) DEFAULT NULL,
  `teacher_id` varchar(5) DEFAULT NULL,
  `password` varchar(28) DEFAULT NULL,
  `name_of_subject` varchar(20) DEFAULT NULL,
  `score` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teachers`
--

LOCK TABLES `teachers` WRITE;
/*!40000 ALTER TABLE `teachers` DISABLE KEYS */;
INSERT INTO `teachers` VALUES ('001','0001','123','Английский язык','135'),('002','0002','test_password','русский','1'),('001','0002','123','математика','3'),('123','1233','1','фылврофы',NULL),('101','0001','123','рузгий',NULL);
/*!40000 ALTER TABLE `teachers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timetable`
--

DROP TABLE IF EXISTS `timetable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timetable` (
  `school_id` varchar(4) DEFAULT NULL,
  `grade_id` varchar(4) DEFAULT NULL,
  `Mon` varchar(128) DEFAULT NULL,
  `Tue` varchar(128) DEFAULT NULL,
  `Wed` varchar(128) DEFAULT NULL,
  `Thu` varchar(128) DEFAULT NULL,
  `Fri` varchar(128) DEFAULT NULL,
  `Sat` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timetable`
--

LOCK TABLES `timetable` WRITE;
/*!40000 ALTER TABLE `timetable` DISABLE KEYS */;
INSERT INTO `timetable` VALUES ('001','001','Русский язык\nАнглийский язык\nМатематика\n','Привет\nУрок\nКекс\n','Математика\nУкраинский язык\nМатематика\n','ИЗО\nФиз-ра\nМатематика\n','Труды\nУкраинский язык\nМатематика\n','Русский язык\nАнглийский язык\nМатематика\n'),('001','002','Русский язык\nАнглийский язык\nМатематика\n','Английский язык\nРусский язык\nМатематика\n','Математика\nУкраинский язык\nМатематика\n','ИЗО\nФиз-ра\nМатематика\n','Труды\nУкраинский язык\nМатематика\n','Русский язык\nАнглийский язык\nМатематика\n'),('002','001','Русский язык\nАнглийский язык\nМатематика\n','Английский язык\nРусский язык\nМатематика\n','Математика\nУкраинский язык\nМатематика\n','ИЗО\nФиз-ра\nМатематика\n','Труды\nУкраинский язык\nМатематика\n','Русский язык\nАнглийский язык\nМатематика\n'),('002','002','Русский язык\nАнглийский язык\nМатематика\n','Английский язык\nРусский язык\nМатематика\n','Математика\nУкраинский язык\nМатематика\n','ИЗО\nФиз-ра\nМатематика\n','Труды\nУкраинский язык\nМатематика\n','Русский язык\nАнглийский язык\nМатематика\n'),('1','2',NULL,NULL,NULL,NULL,NULL,NULL),('001','003','кекс1\nкекс2\n','кекс1\nкекс2\n','кекс1\nкекс2\n','кекс1\nкекс2\n','кекс1\nкекс2\n','кекс1\nкекс2\n'),('123','001',NULL,NULL,NULL,NULL,NULL,NULL),('123','002','Лол\nКек\nЧебурек\n\n','Лол\nКек\nЧебурек\n\n','Лол\nКек\nЧебурек\n\n','Лол\nКек\nЧебурек\n\n','Лол\nКек\nЧебурек\n\n','Лол\nКек\nЧебурек\n\n'),('123','003',NULL,NULL,NULL,NULL,NULL,NULL),('101','001',NULL,NULL,NULL,NULL,NULL,NULL),('101','002',NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `timetable` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-09-16 21:46:18
