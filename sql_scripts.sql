USE skellig_uns_lab_equipment;

-- DROP TABLE ph_records;
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
 COMMIT;