CREATE DATABASE IF NOT EXISTS NMAP;
USE NMAP;
CREATE TABLE maquinas(
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    ip VARCHAR(15) NOT NULL
);
CREATE TABLE usuarios(
	usuario VARCHAR(100) NOT NULL PRIMARY KEY,
    pass VARCHAR(256) NOT NULL,
    salt VARCHAR(30),
    tokens INT(2) NOT NULL
);

INSERT INTO `maquinas` (`nombre`, `ip`) VALUES ('DEBIAN_9.0', '10.227.87.26');

INSERT INTO `maquinas` (`nombre`, `ip`) VALUES ('UBUNTU_22.04', '10.227.87.19');

INSERT INTO `maquinas` (`nombre`, `ip`) VALUES ('BACKUP_SERVER', '10.227.87.29');

INSERT INTO `maquinas` (`nombre`, `ip`) VALUES ('ORACLE_SQL_SERVER', '10.227.87.21');

INSERT INTO `maquinas` (`nombre`, `ip`) VALUES ('MARIADB', '10.227.87.31');