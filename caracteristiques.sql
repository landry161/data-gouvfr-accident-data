CREATE TABLE `caracteristiques` (
 `id` int NOT NULL AUTO_INCREMENT,
 `accident_id` bigint NOT NULL,
 `date_accident` date NOT NULL,
 `heure` varchar(10) COLLATE utf8mb3_unicode_ci NOT NULL,
 `conditions` text COLLATE utf8mb3_unicode_ci NOT NULL,
 `departement` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
 `commune` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
 `localisation` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
 `intersection` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
 `conditions_atmospheriques` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
 `collision` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
 `adresse` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
 `lat` float NOT NULL,
 `lng` float NOT NULL,
 `mois` varchar(25) COLLATE utf8mb3_unicode_ci NOT NULL,
 PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=55303 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_c