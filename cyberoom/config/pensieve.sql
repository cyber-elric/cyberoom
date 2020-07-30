-- MySQL dump 10.13  Distrib 8.0.20, for Linux (x86_64)
--
-- Host: localhost    Database: cyberoom
-- ------------------------------------------------------
-- Server version	8.0.20-0ubuntu0.20.04.1

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
-- Table structure for table `pensieve_pensieve`
--

DROP TABLE IF EXISTS `pensieve_pensieve`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pensieve_pensieve` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(66) NOT NULL,
  `content` longtext NOT NULL,
  `upDate` datetime(6) NOT NULL,
  `up_id` varchar(60) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  KEY `pensieve_pensieve_up_id_43ed83d4` (`up_id`),
  CONSTRAINT `pensieve_pensieve_up_id_43ed83d4_fk_gate_thekey_owner` FOREIGN KEY (`up_id`) REFERENCES `gate_thekey` (`owner`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pensieve_pensieve`
--

LOCK TABLES `pensieve_pensieve` WRITE;
/*!40000 ALTER TABLE `pensieve_pensieve` DISABLE KEYS */;
INSERT INTO `pensieve_pensieve` VALUES (2,'Wireless','未来：无线技术\r\n\r\n无线传输、连接\r\n无线充电、供电\r\n\r\n节省线材\r\n干扰、安全\r\n效率问题','2020-07-15 05:47:08.332056','elric'),(3,'Cooling and Heat','发热与散热问题对性能的影响','2020-07-15 05:48:01.238542','elric'),(4,'Power','电池续航能力、体积、寿命\r\n\r\n新能源','2020-07-15 05:49:01.622995','elric'),(5,'Gaming','比起开发工具类、社区类的网站或软件\r\n开发游戏更容易变现\r\n游戏也是一种消耗品，一个游戏通关了，就要玩下一个游戏，像Dota、网游、手游那些，虽然寿命较长，但也有会终点；\r\n游戏算是目前比较好的一种娱乐消遣方式，发展空间还是有的；\r\n手游、网络那种长期运营的游戏不太适合独立开发者吧，还是独立游戏吧。','2020-07-15 05:55:11.222134','elric'),(6,'Food','吃饭是一个大问题\r\n花多少钱、健不健康、要用多少时间吃、人要多少时间做、外卖要多长时间才送来。\r\n\r\n一种快捷简单的食物，做成饼干，药丸等形状，\r\n解决能量需求，不会有饥饿感；缩短在吃饭上花的时间；降低健康饮食的门槛，不用花时间花心思去研究营养学。\r\n\r\n技术、成本\r\n人类长期只吃这种食物的反应（生理与心理）；对美食的需求\r\n\r\n龙珠：仙豆','2020-07-15 06:04:02.844902','elric'),(7,'膜','海贼王 香波地岛 人鱼岛 泡泡膜\r\n\r\n取代雨伞、雨衣、雨靴\r\n\r\n\r\n\r\n潜水','2020-07-15 06:09:05.005671','elric'),(8,'Room','让老鼠、蟑螂、蚊子、苍蝇、蚂蚁、壁虎、飞虫之类的生物远离住宅\r\n\r\n超级加强版蚊香的功能，不一定是蚊香这类产品，不一定是通过生化的方式','2020-07-15 06:13:44.889157','elric'),(9,'AI','Artificial Intelligence\r\n\r\nthe future','2020-07-15 06:15:25.101513','elric'),(10,'Driverless & AI & Big Data','new traffic system\r\nauto\r\npublic transportation','2020-07-15 06:17:59.284981','elric'),(11,'Auto、Intelligent、Recommend','微软开机登陆界面壁纸\r\nbing每日一图\r\n自动亮度\r\n自动清晰度\r\n。。。','2020-07-16 01:31:34.806566','elric'),(12,'Time','时停、局部时停、\r\n时间加速或回溯（触摸触发、光环效果）\r\n穿越、轮回\r\n\r\n\r\nthe world、绯红之王、crazy diamond、败者食尘、虚空、蚂蚁、长生仙体、海贼王','2020-07-22 07:45:00.049820','elric'),(14,'deng1.0','卡进度，将内容故意分成几天发布；\r\n故意用没意思的内容增长游戏时间；\r\n\r\n养成','2020-07-25 11:34:29.760586','elric');
/*!40000 ALTER TABLE `pensieve_pensieve` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-07-29  9:55:52
