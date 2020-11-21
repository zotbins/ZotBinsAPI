USE zotbins$zotbins;
DROP TABLE IF EXISTS Error;
CREATE TABLE Error(
									id INT NOT NULL AUTO_INCREMENT,
									timestamp DATETIME NOT NULL,
									sensor_id VARCHAR(30) NOT NULL,
									error VARCHAR(500) NOT NULL,
									PRIMARY KEY (id));