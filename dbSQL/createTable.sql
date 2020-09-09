CREATE TABLE public.sensor
(
    id serial NOT NULL,
	temp real NOT NULL,
    umid real NOT NULL,
    "timestamp" real,
    CONSTRAINT sensor_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.sensor
    OWNER to pi;
