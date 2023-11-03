CREATE TABLE `vehicules` (
 `id` bigint NOT NULL AUTO_INCREMENT,
 `accident_id` bigint NOT NULL,
 `vehicule_id` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
 `numero_vehicule` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
 `categorie_vehicule` varchar(250) COLLATE utf8mb3_unicode_ci NOT NULL,
 `motorisation` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
 PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=94494 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci