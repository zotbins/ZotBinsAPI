USE gschoe$zotbins;
DROP TABLE IF EXISTS Frequency;
CREATE TABLE Frequency(
									id INT NOT NULL AUTO_INCREMENT,
									timestamp DATETIME NOT NULL,
									sensor_id VARCHAR(30) NOT NULL,
									PRIMARY KEY (id));
                                    
-- CREATE TABLE Frequency(id INT NOT NULL AUTO_INCREMENT, timestamp DATETIME NOT NULL, sensor_id VARCHAR(30) NOT NULL, PRIMARY KEY (id));