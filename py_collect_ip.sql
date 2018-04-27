DROP TABLE IF EXISTS `collect_ips`;
CREATE TABLE `collect_ips` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `host` VARCHAR(15) NOT NULL COMMENT 'XXX.XXX.XXX.XXX',
  `port` SMALLINT UNSIGNED NOT NULL COMMENT '<= 65536',
  `type` VARCHAR(5) NOT NULL COMMENT 'http 或 https',
  `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态(1-有效 0-无效)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `collect_ips_host_port_unique` (`host`, `port`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;