USE zotbins$zotbins;
DROP TABLE IF EXISTS Sensors;
CREATE TABLE Sensors(
	sid VARCHAR(30),
    did VARCHAR(30),
    type INT NOT NULL,
    name VARCHAR(20),
    FOREIGN KEY (did) REFERENCES Devices(id) ON DELETE CASCADE,
    PRIMARY KEY (sid));