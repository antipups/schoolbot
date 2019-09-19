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
  `invite_url` varchar(45) DEFAULT NULL,
  `bulletin_board` varchar(1024) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grades`
--

LOCK TABLES `grades` WRITE;
/*!40000 ALTER TABLE `grades` DISABLE KEYS */;
INSERT INTO `grades` VALUES ('001','10а','001','img\\001001.png','keksij','-1','Доска объявлений, тестовая.\n\n\nУПс ай диднт егейн\n\n\nПривет'),('001','11а','002','img\\учитель.jpg','Биляшка Ольга','https://t.me/joinchat/KfvRalU_1UaALTop7h_cog','Доска объявлений, тестовая. Для другого класса.'),('002','7а','001','img\\учитель.jpg','Тестовый','-1','Доска объявлений, тестовая.'),('111','5б','019','img\\111019.jpg','Любмила Петровна','-1','Новый класс\n\n\n-1'),('001','10б','19б','img\\00119б.jpg','Людмила Никитишна','-1','Новый класс'),('001','4б','04б','img\\00104б.jpg','Люблю бамбук','https://t.me/joinchat/KfvRalU_1UaALTop7h_cog','Доска объявлений пуста.'),('123','123','ббд','img\\123ббд.png','Куркурина Любовь','-1','Новый класс'),('123','12','001','img\\123001.png','keks','-1','Доска объявлений пуста.'),('123','10д','ббк','img\\123ббк.png','фыв','-1','Новый класс\n\n\nфыролвпфыов'),('124','10а','19а','Новый класс','Новый класс','-1','Новый класс'),('124','10г','10г','img\\12410г.png','Кексич','-1','Новый класс'),('asd','-9','asf','img\\asdasf.png','asf','https://t.me/joinchat/KfvRalU_1UaALTop7h_cog','Новый класс\n\n\nКекс');
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
INSERT INTO `homework` VALUES ('001','001','русский','asd'),('002','001','математика','hello'),('001','002','русский','asd'),('001','001','Физика','asd'),('001','001','математика','номер 343'),('001','003','русский','Новое дз'),('002','001','физика','фыв'),('001','001','Английский язык','hello'),('001','001','литература','keks'),('001','04б','Английский язык','asd'),('001','19б','Английский язык','Приветики'),('123','ббк','кекилогия','так блет');
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
INSERT INTO `marks` VALUES ('001','001','001','русский','4'),('001','001','001','русский','4'),('001','001','001','математика','5'),('001','001','001','математика','2'),('001','001','001','русский','2'),('001','001','002','русский','3'),('001','001','002','русский','2'),('001','001','002','русский','6'),('001','003','123','русский','3'),('001','003','1','русский','5'),('001','003','123','русский','5'),('001','001','001','русский','5'),('001','001','001','русский','5'),('001','001','002','русский','5'),('002','001','002','физика','5'),('002','001','002','физика','3'),('001','001','001','Английский язык','9'),('001','001','001','Английский язык','12'),('001','001','002','литература','3'),('001','001','123','Английский язык','5'),('001','001','001','Английский язык','2'),('123','ббк','кек','кекилогия','5'),('001','001','123','Русский','5'),('001','001','001','Русский','5'),('001','001','003','Физика','5');
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
INSERT INTO `res` VALUES ('картинка1','img\\картинка1.jpg'),('реклама1','кексик'),('картинка2','img\\картинка2.jpg'),('реклама2','кексик 2');
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
INSERT INTO `schools` VALUES ('Самая первая ОШ','Всем здрасти, забор покрасьти.','001','ШОК! Собака съела шарик.\n\n\nПервоклашки поступили в первый класс!\n\n\nВозле 9-а случился пожар! Бегите все!!!\n\n\n'),('ОШ 1234','Мы - топ школа!','002','ШОК! Собака съела шарик.\n\n\nПервоклашки поступили в первый класс!\n\n\n'),('Тестовая школа','Мы лучшие!!!','003','Завтра род. собрание на 9.'),('Вторая тест школа','Новосозданная школа','004','asd'),('Кексик','Крутой текст','005','Крутая афиша'),('Новая шк','Новосозданная школа','101','Сегодня понедельник, ура!!!'),('НЕ ОШай мне','Новосозданная школа','007','Тест\n\n\nПривет'),('Лицей64','Новосозданная школа','123','-1'),('keks','Новосозданная школа','111','-1'),('asjdhasiudhasd','Новосозданная школа','120','asdjhasod'),('Ноунейм','Новосозданная школа','191','-1'),('keksik','Новосозданная школа','124','-1'),('Нормальное название asd','Новосозданная школа','asd','-1\n\n\nНовая новость asd'),('Лицей','Новосозданная школа','asf','Привет');
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
INSERT INTO `students` VALUES ('001','001','Никита Куркурин','001'),('001','001','Сергей Иорданов','002'),('002','001','Коля','002'),('001','003','Николай','123'),('001','003','Николай Смирнов','1'),('001','001','Никитка','123'),('001','001','Никитка','123'),('123','ббк','кексик','123'),('123','ббк','никитка','кек'),('001','001','Максимка','003');
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
INSERT INTO `teachers` VALUES ('001','0001','1','Физика','182'),('002','0002','test_password','русский','1'),('001','0002','123','математика','3'),('123','1233','1','фылврофы',NULL),('101','0001','123','рузгий',NULL),('123','1234','123','Доча',NULL),('001','123','1','литература','5'),('123','0001','1','кекилогия','4'),('kek','keek','1','kek','5'),('asd','asdd','123','asdf','8');
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
INSERT INTO `timetable` VALUES ('001','001','test1\ntest2\n','Привет\nУрок\nКекс\n','Математика\nУкраинский язык\nМатематика\n','ИЗО\nФиз-ра\nМатематика\n','Труды\nУкраинский язык\nМатематика\n','keksik\n'),('001','002','Русский язык\nАнглийский язык\nМатематика\n','Английский язык\nРусский язык\nМатематика\n','Математика\nУкраинский язык\nМатематика\n','ИЗО\nФиз-ра\nМатематика\n','Труды\nУкраинский язык\nМатематика\n','Русский язык\nАнглийский язык\nМатематика\n'),('002','001','Русский язык\nАнглийский язык\nМатематика\n','Английский язык\nРусский язык\nМатематика\n','Математика\nУкраинский язык\nМатематика\n','ИЗО\nФиз-ра\nМатематика\n','Труды\nУкраинский язык\nМатематика\n','Русский язык\nАнглийский язык\nМатематика\n'),('1','2',NULL,NULL,NULL,NULL,NULL,NULL),('001','003','кекс1\nкекс2\n','кекс1\nкекс2\n','кекс1\nкекс2\n','кекс1\nкекс2\n','кекс1\nкекс2\n','кекс1\nкекс2\n'),('101','001',NULL,NULL,NULL,NULL,NULL,NULL),('101','002',NULL,NULL,NULL,NULL,NULL,NULL),('007','001',NULL,NULL,NULL,NULL,NULL,NULL),('111','019',NULL,NULL,NULL,NULL,NULL,NULL),('001','19б',NULL,NULL,NULL,NULL,NULL,NULL),('001','04б',NULL,NULL,NULL,NULL,NULL,NULL),('123','ббд',NULL,NULL,NULL,NULL,NULL,NULL),('123','001',NULL,NULL,NULL,NULL,NULL,NULL),('123','ббк',NULL,NULL,NULL,NULL,NULL,NULL),('124','19а',NULL,NULL,NULL,NULL,NULL,NULL),('124','10г',NULL,NULL,NULL,NULL,NULL,NULL),('asd','asf',NULL,NULL,NULL,NULL,NULL,NULL);
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

-- Dump completed on 2019-09-18 18:26:32
