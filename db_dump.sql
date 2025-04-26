-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: localhost    Database: zavio_rewards
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.22.04.1

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
-- Table structure for table `nodes`
--

DROP TABLE IF EXISTS `nodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nodes` (
  `node_id` int NOT NULL AUTO_INCREMENT,
  `status` enum('active','reserved','inactive') COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_nodes` int NOT NULL,
  `daily_reward` int DEFAULT NULL,
  `date_updated` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`node_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nodes`
--

LOCK TABLES `nodes` WRITE;
/*!40000 ALTER TABLE `nodes` DISABLE KEYS */;
INSERT INTO `nodes` VALUES (1,'inactive',10000,NULL,'2025-04-10 15:25:27'),(2,'active',9000,150000,'2025-04-10 15:25:27'),(3,'reserved',1000,0,'2025-04-26 08:46:52');
/*!40000 ALTER TABLE `nodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `total_daily_reward`
--

DROP TABLE IF EXISTS `total_daily_reward`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `total_daily_reward` (
  `id` int NOT NULL,
  `total_reward` int NOT NULL,
  `update_date` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `total_daily_reward`
--

LOCK TABLES `total_daily_reward` WRITE;
/*!40000 ALTER TABLE `total_daily_reward` DISABLE KEYS */;
INSERT INTO `total_daily_reward` VALUES (1,150000,'2025-04-21 11:47:08',1);
/*!40000 ALTER TABLE `total_daily_reward` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `tokens_redeemed` int NOT NULL,
  `transaction_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `transaction_status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `wallet_address` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `polygon_tx_hash` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `blockchain_timestamp` datetime DEFAULT NULL,
  `blockchain_status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`transaction_id`),
  UNIQUE KEY `polygon_tx_hash` (`polygon_tx_hash`),
  KEY `transactions_user_id_fkey` (`user_id`),
  CONSTRAINT `transactions_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,2,5625,'2025-04-21 16:42:35','success','XTXTXTXTXTXTXTX','VSVSVSVSVSSV','2025-04-21 16:42:35','active');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_nodes`
--

DROP TABLE IF EXISTS `user_nodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_nodes` (
  `user_node_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `nodes_assigned` int NOT NULL,
  `date_assigned` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_node_id`),
  KEY `user_nodes_user_id_fkey` (`user_id`),
  CONSTRAINT `user_nodes_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_nodes`
--

LOCK TABLES `user_nodes` WRITE;
/*!40000 ALTER TABLE `user_nodes` DISABLE KEYS */;
INSERT INTO `user_nodes` VALUES (1,2,5,'2025-04-10 15:25:27'),(2,3,15,'2025-04-10 15:25:27'),(3,4,7,'2025-04-10 15:25:27'),(4,5,3,'2025-04-10 15:25:27'),(5,6,8,'2025-04-10 15:25:27'),(6,7,1,'2025-04-10 15:25:27'),(7,8,6,'2025-04-10 15:25:27'),(8,9,2,'2025-04-10 15:25:27'),(9,10,25,'2025-04-10 15:25:27'),(11,1,1000,'2025-04-18 16:35:06');
/*!40000 ALTER TABLE `user_nodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_points`
--

DROP TABLE IF EXISTS `user_points`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_points` (
  `user_points_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `total_points` int NOT NULL,
  `available_for_redemtion` int NOT NULL,
  `zavio_token_rewarded` int NOT NULL,
  `date_updated` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_points_id`),
  KEY `user_points_user_id_fkey` (`user_id`),
  CONSTRAINT `user_points_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_points`
--

LOCK TABLES `user_points` WRITE;
/*!40000 ALTER TABLE `user_points` DISABLE KEYS */;
INSERT INTO `user_points` VALUES (1,2,18250,12625,5625,'2025-04-21 14:28:35');
/*!40000 ALTER TABLE `user_points` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_reward_activity`
--

DROP TABLE IF EXISTS `user_reward_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_reward_activity` (
  `activity_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `points` int NOT NULL,
  `type` enum('reward','redemption','bonus') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `isCredit` tinyint(1) DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `activity_timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`activity_id`),
  KEY `user_reward_activity_user_id_fkey` (`user_id`),
  CONSTRAINT `user_reward_activity_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_reward_activity`
--

LOCK TABLES `user_reward_activity` WRITE;
/*!40000 ALTER TABLE `user_reward_activity` DISABLE KEYS */;
INSERT INTO `user_reward_activity` VALUES (1,2,75,'reward',1,'Daily rewarded nodes','2025-04-10 15:25:27'),(2,3,225,'reward',1,'Nodes rewarded for active participation','2025-04-10 15:25:27'),(3,4,105,'reward',1,'Nodes rewarded for active participation','2025-04-10 15:25:27'),(4,5,45,'reward',1,'Nodes rewarded for active participation','2025-04-10 15:25:27'),(5,6,120,'reward',1,'Nodes rewarded for active participation','2025-04-10 15:25:27'),(6,7,15,'reward',1,'Nodes rewarded for active participation','2025-04-10 15:25:27'),(7,8,90,'reward',1,'Nodes rewarded for active participation','2025-04-10 15:25:27'),(8,9,30,'reward',1,'Nodes rewarded for active participation','2025-04-10 15:25:27'),(9,10,375,'reward',1,'Nodes rewarded for active participation','2025-04-10 15:25:27'),(10,2,75,'reward',1,'Daily rewarded nodes','2025-04-11 15:25:27'),(11,2,5,'reward',1,'Nodes starting balance','2025-04-09 15:25:27'),(12,2,75,'reward',1,'Daily rewarded nodes','2025-04-10 15:25:27'),(13,2,5625,'redemption',0,'Tokens redeemed','2025-04-10 15:25:27');
/*!40000 ALTER TABLE `user_reward_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` text COLLATE utf8mb4_unicode_ci,
  `registration_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `last_login` datetime DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'active',
  `role` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'user',
  `import_status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `reset_password_token` text COLLATE utf8mb4_unicode_ci,
  `token_expiry` datetime DEFAULT NULL,
  `is_first_time_login` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Mike','mike@example.com','$2b$12$wbdGI2ZwLkrZAe2.wwVZdua4VgRkt4TccUuJtMW4PRaKkWVJP0iUe','2025-04-10 15:25:27',NULL,'active','admin','completed',NULL,NULL,0),(2,'Test user 1','testuser1@example.com','$2b$12$eHY9HlqeQbjfikDFaB.Nle3LTABbyyMmg.XwVcDz/wf9KnEdEqxBG','2025-04-10 15:25:27',NULL,'active','user','completed',NULL,NULL,0),(3,'Test user 2','testuser2@example.com','$2a$12$gvGKg5cACn4zY./HMxFm5u3QTotdUNUY27t4mTGbvx2/EeWXVjG3m','2025-04-10 15:25:27',NULL,'active','user','pending',NULL,NULL,1),(4,'Test user 3','testuser3@example.com','$2a$12$gvGKg5cACn4zY./HMxFm5u3QTotdUNUY27t4mTGbvx2/EeWXVjG3m','2025-04-10 15:25:27',NULL,'active','user','pending',NULL,NULL,1),(5,'Test user 4','testuser4@example.com','$2a$12$gvGKg5cACn4zY./HMxFm5u3QTotdUNUY27t4mTGbvx2/EeWXVjG3m','2025-04-10 15:25:27',NULL,'active','user','pending',NULL,NULL,1),(6,'Test user 5','testuser5@example.com','$2a$12$gvGKg5cACn4zY./HMxFm5u3QTotdUNUY27t4mTGbvx2/EeWXVjG3m','2025-04-10 15:25:27',NULL,'active','user','pending',NULL,NULL,1),(7,'Test user 6','testuser6@example.com','$2a$12$gvGKg5cACn4zY./HMxFm5u3QTotdUNUY27t4mTGbvx2/EeWXVjG3m','2025-04-10 15:25:27',NULL,'active','user','pending',NULL,NULL,1),(8,'Test user 7','testuser7@example.com','$2a$12$gvGKg5cACn4zY./HMxFm5u3QTotdUNUY27t4mTGbvx2/EeWXVjG3m','2025-04-10 15:25:27',NULL,'active','user','pending',NULL,NULL,1),(9,'Test user 8','testuser8@example.com','$2a$12$gvGKg5cACn4zY./HMxFm5u3QTotdUNUY27t4mTGbvx2/EeWXVjG3m','2025-04-10 15:25:27',NULL,'active','user','pending',NULL,NULL,1),(10,'Test user 9','testuser9@example.com','$2a$12$gvGKg5cACn4zY./HMxFm5u3QTotdUNUY27t4mTGbvx2/EeWXVjG3m','2025-04-10 15:25:27',NULL,'active','user','pending',NULL,NULL,1),(11,'Test user 10','testuser10@example.com','$2a$12$gvGKg5cACn4zY./HMxFm5u3QTotdUNUY27t4mTGbvx2/EeWXVjG3m','2025-04-10 15:25:27',NULL,'active','user','pending',NULL,NULL,1),(18,'Test User','test1@test.com','$2b$12$af8MdcXQhv8RRV1767r1TeaQQpvhn8BO4B/IJPSD49CbK870BqX.W','2025-04-22 13:26:26',NULL,'active','user',NULL,NULL,NULL,0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wallets`
--

DROP TABLE IF EXISTS `wallets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wallets` (
  `wallet_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `wallet_address` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `wallet_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`wallet_id`),
  UNIQUE KEY `wallet_address` (`wallet_address`),
  KEY `wallets_user_id_fkey` (`user_id`),
  CONSTRAINT `wallets_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wallets`
--

LOCK TABLES `wallets` WRITE;
/*!40000 ALTER TABLE `wallets` DISABLE KEYS */;
INSERT INTO `wallets` VALUES (1,1,'0x12345','Polygon (ERC-20) ','2025-04-10 15:25:27'),(2,2,'0x742d35Cc6634C0532925a3b844Bc454e4438f44E','Polygon (ERC-20) ','2025-04-10 15:25:27'),(3,3,'0xABCDE','Polygon (ERC-20) ','2025-04-10 15:25:27'),(4,4,'0xFGHIJ','Polygon (ERC-20) ','2025-04-10 15:25:27'),(5,5,'0xKLMNO','Polygon (ERC-20) ','2025-04-10 15:25:27'),(6,6,'0xPQRST','Polygon (ERC-20) ','2025-04-10 15:25:27'),(7,7,'0xUVWXY','Polygon (ERC-20) ','2025-04-10 15:25:27'),(8,8,'0xZABCD','Polygon (ERC-20) ','2025-04-10 15:25:27'),(9,9,'0xEFGHI','Polygon (ERC-20) ','2025-04-10 15:25:27'),(10,10,'0xJKLMN','Polygon (ERC-20) ','2025-04-10 15:25:27');
/*!40000 ALTER TABLE `wallets` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-26 13:58:06
