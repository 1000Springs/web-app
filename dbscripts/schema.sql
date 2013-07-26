
CREATE TABLE `images` (
  `image_id` int(11) NOT NULL,
  `sample_id` int(11) DEFAULT NULL,
  `image_path` text NOT NULL,
  `image_name` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`image_id`)
); 



CREATE TABLE `location` (
  `FEATURE_NC` varchar(100) NOT NULL DEFAULT '',
  `COMMON_FEATURE_NAME` text,
  `eastings` double DEFAULT NULL,
  `northings` double DEFAULT NULL,
  `FEATURE_SYSTEM` text,
  `description` text,
  `toilet` tinyint(1) DEFAULT NULL,
  `parkbench` tinyint(1) DEFAULT NULL,
  `track` tinyint(1) DEFAULT NULL,
  `private` tinyint(1) DEFAULT NULL,
  `colour` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`FEATURE_NC`)
);



CREATE TABLE `physical_data` (
  `SAMPLE_ID` int(11) NOT NULL DEFAULT '0',
  `PHYS_ID` int(11) NOT NULL DEFAULT '0',
  `TEMPERATURE` float DEFAULT NULL,
  `PH_LEVEL` float DEFAULT NULL,
  `REDOX` float DEFAULT NULL,
  `DISSOLVED_OXYGEN` float DEFAULT NULL,
  `CONDUCTIVITY` float DEFAULT NULL,
  `DATE_GATHERED` date DEFAULT NULL,
  PRIMARY KEY (`SAMPLE_ID`,`PHYS_ID`),
  CONSTRAINT `FK_PHYSICAL_SAMPLE_ID` FOREIGN KEY (`SAMPLE_ID`) REFERENCES `sample` (`SAMPLE_ID`)
);

CREATE TABLE `sample` (
  `SAMPLE_ID` int(11) NOT NULL DEFAULT '0',
  `date_gathered` date DEFAULT NULL,
  `LOCATION_FEATURE_NC` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`SAMPLE_ID`),
  KEY `FK_SAMPLE_FEATURE_NC` (`LOCATION_FEATURE_NC`),
  CONSTRAINT `FK_SAMPLE_FEATURE_NC` FOREIGN KEY (`LOCATION_FEATURE_NC`) REFERENCES `location` (`FEATURE_NC`)
);




CREATE TABLE `user` (
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`username`)
) ;


