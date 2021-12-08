USE skellig_uns_lab_equipment;

-- DROP TABLE ph_records;
-- DROP TABLE shaker_records;
-- DROP TABLE conductivity_records;
DROP TABLE viscometer_records;
-- DELETE FROM shaker_records;
-- COMMIT;

 CREATE TABLE IF NOT EXISTS ph_records(
	record_id INT NOT NULL AUTO_INCREMENT,
    date_logged TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    value FLOAT,
    unit VARCHAR(2),
    temp FLOAT,
    temp_unit VARCHAR(1),
    temp_device VARCHAR(4),
    PRIMARY KEY(record_id)
 );
  CREATE TABLE IF NOT EXISTS shaker_records(
	record_id INT NOT NULL AUTO_INCREMENT,
    date_logged TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    speed FLOAT,
    unit VARCHAR(3),
    PRIMARY KEY(record_id)
 );

 CREATE TABLE IF NOT EXISTS printer_records(
	record_id INT NOT NULL AUTO_INCREMENT,
    date_logged TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    weight FLOAT,
    unit VARCHAR(3),
    PRIMARY KEY(record_id)
 );

  CREATE TABLE IF NOT EXISTS conductivity_records(
	record_id INT NOT NULL AUTO_INCREMENT,
    date_logged DATETIME,
    value FLOAT,
    unit VARCHAR(4),
    secondary_value FLOAT,
    secondary_unit VARCHAR(4),
    PRIMARY KEY(record_id)
 );

 CREATE TABLE IF NOT EXISTS viscometer_records(
	record_id INT NOT NULL AUTO_INCREMENT,
    date_logged TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    rpm FLOAT,
    M VARCHAR(4),
    cP FLOAT,
    S FLOAT,
    D_CM2 FLOAT,
    1_SEC FLOAT,
    temperature FLOAT,
    temp_unit VARCHAR(1),
    Z TIME,
    percentage FLOAT,
    PRIMARY KEY(record_id)
 );
 COMMIT;
 -- SELECT * FROM ph_records;
 
 -- select *from ph_records ORDER BY record_id DESC LIMIT 1;