# db101

## Schema for CheckIns
-- restaurants_analysis.CheckIns definition

CREATE TABLE `CheckIns` (
  `checkin_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `restaurant_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `checkin_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`checkin_id`),
  UNIQUE KEY `checkin_id` (`checkin_id`),
  KEY `restaurant_id` (`restaurant_id`),
  CONSTRAINT `CheckIns_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `Restaurants` (`restaurant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=58974 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


## Schema for CheckIns
-- restaurants_analysis.Inspections definition

CREATE TABLE `Inspections` (
  `inspection_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `restaurant_id` int DEFAULT NULL,
  `violation_description` text,
  `score` int DEFAULT NULL,
  `grade` char(1) DEFAULT NULL,
  `CAMIS` bigint NOT NULL,
  PRIMARY KEY (`inspection_id`),
  UNIQUE KEY `inspection_id` (`inspection_id`),
  KEY `restaurant_id` (`restaurant_id`),
  KEY `Inspections_Restaurants_FK` (`CAMIS`),
  CONSTRAINT `Inspections_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `Restaurants` (`restaurant_id`),
  CONSTRAINT `Inspections_Restaurants_FK` FOREIGN KEY (`CAMIS`) REFERENCES `Restaurants` (`CAMIS`)
) ENGINE=InnoDB AUTO_INCREMENT=121908 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


## Schema for CheckIns
-- restaurants_analysis.Restaurants definition

CREATE TABLE `Restaurants` (
  `restaurant_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `location` point DEFAULT NULL,
  `cuisine_type` varchar(50) DEFAULT NULL,
  `CAMIS` bigint NOT NULL,
  PRIMARY KEY (`restaurant_id`),
  UNIQUE KEY `restaurant_id` (`restaurant_id`),
  UNIQUE KEY `Restaurants_UNIQUE` (`CAMIS`)
) ENGINE=InnoDB AUTO_INCREMENT=25956 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

## Schema for RestaurantCheckinSummary
-- restaurants_analysis.RestaurantCheckinSummary definition

CREATE TABLE `RestaurantCheckinSummary` (
  `restaurant_id` int DEFAULT NULL,
  `checkin_count` bigint NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
