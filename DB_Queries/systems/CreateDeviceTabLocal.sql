USE gschoe$zotbins;
DROP TABLE IF EXISTS Devices;
CREATE TABLE Devices(
		id VARCHAR(30),
        type INT NOT NULL,
        name VARCHAR(20),
        x FLOAT NOT NULL,
        y FLOAT NOT NULL,
        PRIMARY KEY (id));
-- CREATE TABLE Device(id VARCHAR(20), type INT NOT NULL, name VARCHAR(20), x FLOAT NOT NULL, y FLOAT NOT NULL, PRIMARY KEY (id))