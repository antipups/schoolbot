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
INSERT INTO `grades` VALUES ('001','10а','001','img\\001001.png','keksij','-1','Доска объявлений, тестовая.\n\n\nУПс ай диднт егейн\n\n\nПривет'),('001','11а','002','img\\учитель.jpg','Биляшка Ольга','https://t.me/joinchat/KfvRalU_1UaALTop7h_cog','Доска объявлений, тестовая. Для другого класса.'),('002','7а','001','img\\учитель.jpg','Тестовый','-1','Доска объявлений, тестовая.'),('111','5б','019','img\\111019.jpg','Любмила Петровна','-1','Новый класс\n\n\n-1'),('001','10б','19б','img\\00119б.jpg','Людмила Никитишна','-1','Новый класс'),('001','4б','04б','img\\00104б.jpg','Люблю бамбук','https://t.me/joinchat/KfvRalU_1UaALTop7h_cog','Доска объявлений пуста.'),('123','123','ббд','img\\123ббд.png','Куркурина Любовь','-1','Новый класс'),('123','12','001','img\\123001.png','keks','-1','Доска объявлений пуста.'),('123','10д','ббк','img\\123ббк.png','фыв','-1','Новый класс\n\n\nфыролвпфыов'),('124','10а','19а','Новый класс','Новый класс','-1','Новый класс'),('124','10г','10г','img\\12410г.png','Кексич','-1','Новый класс'),('asd','-9','asf','img\\asdasf.png','asf','https://t.me/joinchat/KfvRalU_1UaALTop7h_cog','Новый класс\n\n\nКекс'),('123','5б','090','Новый класс','Новый класс','-1','Новый класс');
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
INSERT INTO `homework` VALUES ('001','001','русский','хочу спатки'),('002','001','математика','hello'),('001','002','русский','asd'),('001','001','Физика','asd'),('001','001','математика','номер 343'),('001','003','русский','Новое дз'),('002','001','физика','фыв'),('001','001','Английский язык','hello'),('001','001','литература','keks'),('001','04б','Английский язык','asd'),('001','19б','Английский язык','Приветики'),('123','ббк','кекилогия','так блет'),('001','001','russian','keks'),('001','001','русский','хочу спатки'),('001','001','математика','пример 1, 2'),('001','001','фывол','фыв'),('001','001','новый предмет','дз по новому предмету'),('001','001','Щявель','привет'),('001','001','2','привет'),('001','001','щявель','привет'),('001','001','фывлофпывшорфыв','фыв'),('001','001','/room','фывдлфоывщшдфывшщфыв'),('001','001','/room','фыошврфыв'),('001','001','нерусский','5'),('001','001','норвегия','фыв'),('001','001','лол','новое задание'),('001','001','лол','не лол'),('001','001','кул','приветх3');
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
  `stud_id` varchar(7) DEFAULT NULL,
  `name_of_subject` varchar(32) DEFAULT NULL,
  `mark` varchar(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marks`
--

LOCK TABLES `marks` WRITE;
/*!40000 ALTER TABLE `marks` DISABLE KEYS */;
INSERT INTO `marks` VALUES ('001','001','2909кн','русский','5'),('001','001','2909кн','русский','4'),('001','001','2303си','русский','5'),('001','001','2303си','русский','5'),('001','001','2909кн','к10а','5'),('001','001','2303си','тестовый','3'),('001','001','2909кн','тестовый','3'),('001','001','2909кн','кекс','5'),('001','001','2909кн','кекс','4'),('001','001','2909кн','русский','3'),('001','001','2909кн','тестовый','4'),('001','001','2909кн','2','2'),('001','001','2909кн','5','5'),('001','001','2303си','5','3'),('001','001','2909кн','5','5'),('001','001','2909кн','норвегия','5'),('001','001','2909кн','лол','5'),('001','001','2909кн','русский','22'),('001','001','2909кн','кул','3'),('001','001','2909кн','Кул','3'),('001','001','2303си','кул','5'),('001','001','2909кн','кул','5'),('001','001','2909кн','русский','2');
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
INSERT INTO `res` VALUES ('картинка1','img\\картинка1.jpg'),('реклама1','кексик'),('картинка2','img\\картинка2.jpg'),('реклама2','кексик 2'),('картинка3','img\\картинка3.jpg'),('реклама3','кексик 3'),('картинка4','img\\картинка4.jpg'),('картинка5','img\\картинка5.jpg'),('реклама5','кексик 5'),('реклама4','кексик 4');
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
  `stud_id` varchar(7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES ('001','001','Никита Куркурин','2909кн'),('001','001','Сергей Иорданов','2303си'),('002','001','Петя','2201пк'),('002','001','Коля','2301кл'),('001','002','Петя','2401пл'),('002','002','Коля','2501лк');
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
  `password` varchar(33) DEFAULT NULL,
  `name_of_subject` varchar(32) DEFAULT NULL,
  `score` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teachers`
--

LOCK TABLES `teachers` WRITE;
/*!40000 ALTER TABLE `teachers` DISABLE KEYS */;
INSERT INTO `teachers` VALUES ('001','0001','123','русский','34'),('001','0002','123','русский','0'),('002','0001','123','математика','0'),('002','0002','123','физика','0'),('001','0004','1','что ещё то Четвертый предмет','106'),('001','0003','1','Лулка','106'),('001','0022','1','СТарый новый препод','102'),('001','0024','1','Алгебра','9'),('001','0025','1','Лит-ра','06'),('001','0023','1123','Третий предмет','101'),('001','1234',NULL,NULL,NULL),('001','1235','123','russian','3'),('001','1111','1','рус',NULL),('001','1232','1','kek',NULL),('001','1222','1','1',NULL),('001','1234','1','кр001001','0'),('001','к10а','1','к10а','78'),('001','к3а','1','к3а','8'),('001','0110','1','к3б',NULL);
/*!40000 ALTER TABLE `teachers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test` (
  `text1` tinytext,
  `text2` tinytext,
  `text3` tinytext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test`
--

LOCK TABLES `test` WRITE;
/*!40000 ALTER TABLE `test` DISABLE KEYS */;
INSERT INTO `test` VALUES ('1','kek','sex'),('2','lol','lolx2'),('3','kek3','sex');
/*!40000 ALTER TABLE `test` ENABLE KEYS */;
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
INSERT INTO `timetable` VALUES ('001','001','Русский\nУкраинский\nАнглийский\n','ИЗО\nМатан\nФиз-ра\n','кек1\nкек2\nкек3\n','кек1\nкек2\nкек3\n','кек1\nкек2\nкек3\n','Русский\nМатематика\nИЗО\n\n'),('001','002','Русский\nУкраинский\nАнглийский\n','\r\n002\n','002\n','Русский\nУкраинский\nАнглийский\n','ИЗО\nМатан\nФиз-ра\n','кек1\nкек2\nкек3, кек1\nкек2\nкек3, кек1\nкек2\nкек3, кек1\nкек2\nкек3\n'),('002','001','Русский язык\nАнглийский язык\nМатематика\n','Английский язык\nРусский язык\nМатематика\n','Математика\nУкраинский язык\nМатематика\n','ИЗО\nФиз-ра\nМатематика\n','Труды\nУкраинский язык\nМатематика\n','Русский язык\nАнглийский язык\nМатематика\n'),('1','2',NULL,NULL,NULL,NULL,NULL,NULL),('001','003','кекс1\nкекс2\n','кекс1\nкекс2\n','кекс1\nкекс2\n','кекс1\nкекс2\n','кекс1\nкекс2\n','кекс1\nкекс2\n'),('101','001',NULL,NULL,NULL,NULL,NULL,NULL),('101','002',NULL,NULL,NULL,NULL,NULL,NULL),('007','001',NULL,NULL,NULL,NULL,NULL,NULL),('111','019',NULL,NULL,NULL,NULL,NULL,NULL),('001','19б',NULL,NULL,NULL,NULL,NULL,NULL),('001','04б',NULL,NULL,NULL,NULL,NULL,NULL),('123','ббд',NULL,NULL,NULL,NULL,NULL,NULL),('123','001',NULL,NULL,NULL,NULL,NULL,NULL),('123','ббк',NULL,NULL,NULL,NULL,NULL,NULL),('124','19а',NULL,NULL,NULL,NULL,NULL,NULL),('124','10г',NULL,NULL,NULL,NULL,NULL,NULL),('asd','asf',NULL,NULL,NULL,NULL,NULL,NULL),('123','090',NULL,NULL,NULL,NULL,NULL,NULL),('002','002','Русский\nУкраинский\nАнглийский\n','ИЗО\nМатан\nФиз-ра\n','кек1\nкек2\nкек3\n','кек1\nкек2\nкек3\n','кек1\nкек2\nкек3\n','кек1\nкек2\nкек3\n');
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

-- Dump completed on 2019-09-29 18:26:49
