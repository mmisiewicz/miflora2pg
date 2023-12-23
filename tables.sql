CREATE TABLE miflora_sensor_assignments (
    id serial NOT NULL,
    name text  NULL,
    assigned_date timestamp with time zone DEFAULT now() NULL,
    mac macaddr  NULL,
    active boolean  NOT NULL);

CREATE TABLE miflora_readings (
    id bigserial NOT NULL,
    sensor_id integer  NULL,
    metric text  NULL,
    metric_value real  NULL,
    reading_date timestamp with time zone  NOT NULL);

CREATE INDEX ON miflora_readings USING BTREE(sensor_id);
CREATE INDEX ON miflora_readings USING BRIN(reading_date);

ALTER TABLE miflora_readings ADD FOREIGN KEY (sensor_id) REFERENCES miflora_sensor_assignments(id);