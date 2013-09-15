
CREATE TABLE `location` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `feature_name` varchar(100) DEFAULT NULL,
  `lat` double DEFAULT NULL,
  `lng` double DEFAULT NULL,
  `feature_system` text,
  `description` text,
  `toilet` tinyint(1) DEFAULT NULL,
  `parkbench` tinyint(1) DEFAULT NULL,
  `track` tinyint(1) DEFAULT NULL,
  `private` tinyint(1) DEFAULT NULL,
  `colour` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `feature_name` (`feature_name`)
);

CREATE TABLE `physical_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `initialTemp` double DEFAULT NULL,
  `pH` double DEFAULT NULL,
  `redox` double DEFAULT NULL,
  `dO` double DEFAULT NULL,
  `conductivity` double DEFAULT NULL,
  `date_gathered` date DEFAULT NULL,
  `size` varchar(20) DEFAULT NULL,
  `colour` varchar(50) DEFAULT NULL,
  `ebullition` varchar(50) DEFAULT NULL,
  `turbidity` double DEFAULT NULL,
  `dnaVolume` double DEFAULT NULL,
  `ferrousIronAbs` double DEFAULT NULL,
  `sampler` varchar(100) DEFAULT NULL,
  `sampleTemp` double DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `sample` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_gathered` date DEFAULT NULL,
  `location_id` int(11) NOT NULL,
  `phys_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_SAMPLE_location` (`location_id`),
  KEY `FK_SAMPLE_phys` (`phys_id`),
  CONSTRAINT `FK_SAMPLE_location` FOREIGN KEY (`location_id`) REFERENCES `location` (`id`),
  CONSTRAINT `FK_SAMPLE_phys` FOREIGN KEY (`phys_id`) REFERENCES `physical_data` (`id`)
);

CREATE TABLE `images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sample_id` int(11) DEFAULT NULL,
  `image_path` text NOT NULL,
  `image_name` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `FK_images_samples` (`sample_id`),
  CONSTRAINT `FK_images_samples` FOREIGN KEY (`sample_id`) REFERENCES `sample` (`id`)
);

CREATE TABLE `user` (
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`username`)
) ;