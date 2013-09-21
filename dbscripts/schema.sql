

CREATE TABLE `location` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `feature_name` varchar(50) DEFAULT NULL,
  `lat` double DEFAULT NULL,
  `lng` double DEFAULT NULL,
  `feature_system` varchar(50) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `toilet` tinyint(1) DEFAULT NULL,
  `parkbench` tinyint(1) DEFAULT NULL,
  `track` tinyint(1) DEFAULT NULL,
  `private` tinyint(1) DEFAULT NULL,
  `colour` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `feature_name` (`feature_name`)
);



delimiter $$

CREATE TABLE `chemical_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Li` float DEFAULT NULL,
  `B` float DEFAULT NULL,
  `N` float DEFAULT NULL,
  `Na` float DEFAULT NULL,
  `P` float DEFAULT NULL,
  `Cl` float DEFAULT NULL,
  `C` float DEFAULT NULL,
  `Al` float DEFAULT NULL,
  `Si` float DEFAULT NULL,
  `K` float DEFAULT NULL,
  `Ca` float DEFAULT NULL,
  `V` float DEFAULT NULL,
  `Cr` float DEFAULT NULL,
  `Fe` float DEFAULT NULL,
  `Mn` float DEFAULT NULL,
  `cobalt` float DEFAULT NULL,
  `Ni` float DEFAULT NULL,
  `Cu` float DEFAULT NULL,
  `Zn` float DEFAULT NULL,
  `Mg` float DEFAULT NULL,
  `As` float DEFAULT NULL,
  `Se` float DEFAULT NULL,
  `Br` float DEFAULT NULL,
  `Sr` float DEFAULT NULL,
  `Mo` float DEFAULT NULL,
  `Ag` float DEFAULT NULL,
  `Cd` float DEFAULT NULL,
  `In` float DEFAULT NULL,
  `Ba` float DEFAULT NULL,
  `La` float DEFAULT NULL,
  `Ti` float DEFAULT NULL,
  `Pb` float DEFAULT NULL,
  `Bi` float DEFAULT NULL,
  `U` float DEFAULT NULL,
  `CH4` float DEFAULT NULL,
  `H2S` float DEFAULT NULL,
  `H2` float DEFAULT NULL,
  `CO` float DEFAULT NULL,
  `nitrate` float DEFAULT NULL,
  `nitrite` float DEFAULT NULL,
  `ammonium` float DEFAULT NULL,
  `sulfate` float DEFAULT NULL,
  `chloride` float DEFAULT NULL,
  `phosphate` float DEFAULT NULL,
  `iron2` float DEFAULT NULL,
  `bicarbonate` float DEFAULT NULL,
  PRIMARY KEY (`id`)
);




CREATE TABLE `physical_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `initialTemp` double DEFAULT NULL,
  `pH` double DEFAULT NULL,
  `redox` double DEFAULT NULL,
  `dO` double DEFAULT NULL,
  `conductivity` double DEFAULT NULL,
  `date_gathered` datetime DEFAULT NULL,
  `size` varchar(20) DEFAULT NULL,
  `colour` varchar(7) DEFAULT NULL,
  `ebullition` varchar(50) DEFAULT NULL,
  `turbidity` double DEFAULT NULL,
  `dnaVolume` double DEFAULT NULL,
  `ferrousIronAbs` double DEFAULT NULL,
  `sampleTemp` double DEFAULT NULL,
  PRIMARY KEY (`id`)
);





CREATE TABLE `sample` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_gathered` datetime NOT NULL,
  `location_id` int(11) DEFAULT NULL,
  `phys_id` int(11) DEFAULT NULL,
  `sampler` varchar(50) NOT NULL,
  `chem_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_SAMPLE_location` (`location_id`),
  KEY `FK_SAMPLE_phys` (`phys_id`),
  CONSTRAINT `FK_SAMPLE_location` FOREIGN KEY (`location_id`) REFERENCES `location` (`id`),
  CONSTRAINT `FK_SAMPLE_phys` FOREIGN KEY (`phys_id`) REFERENCES `physical_data` (`id`)
);





CREATE TABLE `images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sample_id` int(11) NOT NULL,
  `image_path` varchar(150) NOT NULL,
  `image_name` varchar(150) DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `FK_images_samples` (`sample_id`),
  CONSTRAINT `FK_images_samples` FOREIGN KEY (`sample_id`) REFERENCES `sample` (`id`)
);



CREATE TABLE `user` (
  `username` varchar(100) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`username`)
);


