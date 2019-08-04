CREATE DATABASE IF NOT EXISTS `sorveglianza`;
USE `sorveglianza`;
CREATE TABLE IF NOT EXISTS `accessi` (
`ID` int(11) NOT NULL AUTO_INCREMENT,
`Data` datetime DEFAULT CURRENT_TIMESTAMP,
`fkutente` int(11) DEFAULT NULL,
PRIMARY KEY (`ID`)
);
CREATE TABLE IF NOT EXISTS `allerte` (
`ID` int(11) NOT NULL,
`url_foto` varchar(50) NOT NULL,
`email` varchar(50) NOT NULL,
`tipologia rilevamento` varchar(50) NOT NULL,
`dataora` datetime DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (`ID`)
);
CREATE TABLE IF NOT EXISTS `impostazioni` (
`email` varchar(50) DEFAULT NULL,
`toemail` varchar(50) DEFAULT NULL,
`psw` varchar(50) DEFAULT NULL,
`ID` int(11) DEFAULT NULL,
`motore` int(11) DEFAULT NULL
);
CREATE TABLE IF NOT EXISTS `utente` (
`nome` varchar(50) NOT NULL,
`username` varchar(50) NOT NULL,
`ID` int(11) NOT NULL AUTO_INCREMENT,
`psw` varchar(50) NOT NULL,
`permessi` int(11) NOT NULL,
PRIMARY KEY (`ID`)
);
ALTER TABLE `accessi`
ADD CONSTRAINT `FK_accessi_utente` FOREIGN KEY (`fkutente`) REFERENCES
`utente` (`ID`);

insert into utente(ID,nome,username,psw,permessi) values(default,"marco", "root","root",1);
insert into impostazioni(email,toemail,psw,ID,motore)
values(“youremail@gmail.com”,"emailsent@gmail.com”,"emailpassword",1,1);
