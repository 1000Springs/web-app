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
  `thallium` float DEFAULT NULL,
  `S` float DEFAULT NULL,
  `Rb` float DEFAULT NULL,
  `Cs` float DEFAULT NULL,
  `Hg` float DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `location` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `observation_id` varchar(80) DEFAULT NULL,
  `feature_name` varchar(60) DEFAULT NULL,
  `lat` double DEFAULT NULL,
  `lng` double DEFAULT NULL,
  `feature_system` varchar(50) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `toilet` tinyint(1) DEFAULT NULL,
  `parkbench` tinyint(1) DEFAULT NULL,
  `track` tinyint(1) DEFAULT NULL,
  `private` tinyint(1) DEFAULT NULL,
  `colour` varchar(50) DEFAULT NULL,
  `access` varchar(15) DEFAULT NULL,
  `district` varchar(50) DEFAULT NULL,
  `location` varchar(50) DEFAULT NULL,
  `feature_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `observation_id` (`observation_id`)
) ;

CREATE TABLE `physical_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `initialTemp` double DEFAULT NULL,
  `pH` double DEFAULT NULL,
  `redox` double DEFAULT NULL,
  `dO` double DEFAULT NULL,
  `conductivity` double DEFAULT NULL,
  `size` varchar(20) DEFAULT NULL,
  `colour` varchar(7) DEFAULT NULL,
  `ebullition` varchar(50) DEFAULT NULL,
  `turbidity` double DEFAULT NULL,
  `dnaVolume` double DEFAULT NULL,
  `ferrousIronAbs` double DEFAULT NULL,
  `sampleTemp` double DEFAULT NULL,
  `soilCollected` tinyint(1) DEFAULT NULL,
  `waterColumnCollected` tinyint(1) DEFAULT NULL,
  `gasVolume` double DEFAULT NULL,
  `tds` double DEFAULT NULL,
  `settledAtFourDegC` tinyint(1) DEFAULT NULL
  PRIMARY KEY (`id`)
);

CREATE TABLE `sample` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sample_number` varchar(10) NOT NULL,
  `date_gathered` datetime NOT NULL,
  `location_id` int(11) DEFAULT NULL,
  `phys_id` int(11) DEFAULT NULL,
  `sampler` varchar(50) NOT NULL,
  `chem_id` int(11) DEFAULT NULL,
  `comments` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_SAMPLE_location` (`location_id`),
  KEY `FK_SAMPLE_phys` (`phys_id`),
  KEY `FK_SAMPLE_chem` (`chem_id`),
  CONSTRAINT `FK_SAMPLE_chem` FOREIGN KEY (`chem_id`) REFERENCES `chemical_data` (`id`),
  CONSTRAINT `FK_SAMPLE_location` FOREIGN KEY (`location_id`) REFERENCES `location` (`id`),
  CONSTRAINT `FK_SAMPLE_phys` FOREIGN KEY (`phys_id`) REFERENCES `physical_data` (`id`)
  UNIQUE KEY `sample_number` (`sample_number`)
);

CREATE TABLE `taxonomy` (
  `id` int(11) AUTO_INCREMENT PRIMARY KEY,
  `created_date`     DATETIME DEFAULT CURRENT_TIMESTAMP,
  `last_modified_date` DATETIME ON UPDATE CURRENT_TIMESTAMP,
  `data_file_name` varchar(50) NOT NULL,
  `otu_id` varchar(20) NOT NULL,
  `sequence` varchar(400) DEFAULT NULL,
  `domain` varchar(50) DEFAULT NULL,
  `domain_confidence` double DEFAULT NULL,
  `phylum` varchar(50) DEFAULT NULL,
  `phylum_confidence` double DEFAULT NULL,
  `class` varchar(50) DEFAULT NULL,
  `class_confidence` double DEFAULT NULL,
  `order` varchar(50) DEFAULT NULL,
  `order_confidence` double DEFAULT NULL,
  `family` varchar(50) DEFAULT NULL,
  `family_confidence` double DEFAULT NULL,
  `genus` varchar(50) DEFAULT NULL,
  `genus_confidence` double DEFAULT NULL,
  `species` varchar(50) DEFAULT NULL,
  `species_confidence` double DEFAULT NULL,
  UNIQUE KEY `uk_data_file_name_otu_id` (`data_file_name`,`otu_id`)
);


CREATE TABLE `sample_taxonomy` (
  `id` int(11) AUTO_INCREMENT PRIMARY KEY,
  `sample_id` int(11) NOT NULL,
  `taxonomy_id` int(11) NOT NULL,
  `read_count` int NOT NULL,
  INDEX `idx_sample_taxonomy_sample_id` (`sample_id` ASC),
  CONSTRAINT `fk_st_sample` FOREIGN KEY (`sample_id`) REFERENCES `sample` (`id`),
  CONSTRAINT `fk_st_taxonomy` FOREIGN KEY (`taxonomy_id`) REFERENCES `taxonomy` (`id`),
  UNIQUE KEY `uk_sample_id_taxonomy_id` (`sample_id`,`taxonomy_id`)
);

CREATE OR REPLACE VIEW confident_taxonomy AS (
   select
   `s`.`id` AS `sample_id`,
   `s`.`sample_number` AS `sample_number`,
   sum(`st`.`read_count`) AS `read_count`,
   `t`.`domain` AS `domain`,
   (case when (`t`.`phylum_confidence` >= 0.5) then `t`.`phylum` else NULL end) AS `phylum`,
   (case when (`t`.`class_confidence` >= 0.5) then `t`.`class` else NULL end) AS `class`,
   (case when (`t`.`order_confidence` >= 0.5) then `t`.`order` else NULL end) AS `order`,
   (case when (`t`.`family_confidence` >= 0.5) then `t`.`family` else NULL end) AS `family`,
   (case when (`t`.`genus_confidence` >= 0.5) then `t`.`genus` else NULL end) AS `genus`,
   (
      case when (`t`.`species_confidence` >= 0.5) then `t`.`species` else NULL end
   )
   AS `species`
   from
   (
      (
         `springsdb`.`sample` `s`
         join `springsdb`.`sample_taxonomy` `st` on((`s`.`id` = `st`.`sample_id`))
      )
      join `springsdb`.`taxonomy` `t` on((`st`.`taxonomy_id` = `t`.`id`))
   )
   where (`t`.`domain_confidence` >= 0.5)
   group by `s`.`id`,
   `s`.`sample_number`,
   `t`.`domain`,
   (case when (`t`.`phylum_confidence` >= 0.5) then `t`.`phylum` else NULL end),
   (case when (`t`.`class_confidence` >= 0.5) then `t`.`class` else NULL end),
   (case when (`t`.`order_confidence` >= 0.5) then `t`.`order` else NULL end),
   (case when (`t`.`family_confidence` >= 0.5) then `t`.`family` else NULL end),
   (case when (`t`.`genus_confidence` >= 0.5) then `t`.`genus` else NULL end),
   (
      case when (`t`.`species_confidence` >= 0.5) then `t`.`species` else NULL end
   )
   order by `t`.`domain` desc,
   (case when (`t`.`phylum_confidence` >= 0.5) then `t`.`phylum` else NULL end) desc,
   (case when (`t`.`class_confidence` >= 0.5) then `t`.`class` else NULL end) desc,
   (case when (`t`.`order_confidence` >= 0.5) then `t`.`order` else NULL end) desc,
   (case when (`t`.`family_confidence` >= 0.5) then `t`.`family` else NULL end) desc,
   (case when (`t`.`genus_confidence` >= 0.5) then `t`.`genus` else NULL end) desc,
   (
      case when (`t`.`species_confidence` >= 0.5) then `t`.`species` else NULL end
   )
   desc
);

CREATE TABLE `image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sample_id` int(11) NOT NULL,
  `image_path` varchar(150) NOT NULL,
  `image_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`,`sample_id`),
  KEY `FK_images_samples` (`sample_id`),
  CONSTRAINT `FK_images_samples` FOREIGN KEY (`sample_id`) REFERENCES `sample` (`id`)
);
