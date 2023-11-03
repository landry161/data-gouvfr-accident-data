CREATE TABLE `usagers` (
 `id` int NOT NULL AUTO_INCREMENT,
 `accident_id` bigint NOT NULL,
 `id_usager` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
 `id_vehicule` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
 `numero_vehicule` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
 `categorie_usagers` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
 `gravite` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
 `sexe` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
 `annee_naissance` int NOT NULL,
 `trajet` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
 `securite` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
 `localisation_pieton` varchar(50) COLLATE utf8mb3_unicode_ci NOT NULL,
 PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=126663 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci