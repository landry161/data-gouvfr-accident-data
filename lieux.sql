CREATE TABLE `lieux` (
 `id` int NOT NULL AUTO_INCREMENT,
 `accident_id` bigint NOT NULL,
 `categorie` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
 `regime_circulation` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
 `profil` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
 `plan` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
 `etat_surface` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
 `infrastructure` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
 `situation` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
 `vitesse_max` int NOT NULL,
 PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=55303 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci