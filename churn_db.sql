
CREATE SCHEMA IF NOT EXISTS raw;

SELECT schema_name
FROM information_schema.schemata
WHERE schema_name = 'raw';