USE zotbins$zotbins;
DROP TABLE IF EXISTS WeightDistance;
CREATE TABLE WeightDistance(
									id INT NOT NULL AUTO_INCREMENT,
									timestamp DATETIME NOT NULL,
									sensor_id VARCHAR(30) NOT NULL,
									obs_type INT NOT NULL,
                                    measurement FLOAT,
									PRIMARY KEY (id));
                                    
-- CREATE TABLE WeightDistance(id INT NOT NULL AUTO_INCREMENT, timestamp DATETIME NOT NULL, sensor_id VARCHAR(30) NOT NULL, obs_type INT NOT NULL, measurement FLOAT, PRIMARY KEY (id));