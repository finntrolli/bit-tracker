CREATE TABLE seeder
(
id int NOT NULL AUTO_INCREMENT,
seeder_ip CHAR(15) NOT NULL,
seeeder_port int default 0,
seeder_hostname varchar(255),
torrent CHAR(255) NOT NULL,
hash CHAR(40) NOT NULL,
country_code varchar(45) DEFAULT NULL,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
update_cnt int default 0,
updated TIMESTAMP,
finished TIMESTAMP,
PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;



