
DETACH DATABASE IF EXISTS meu_disco;
ATTACH 'data/loadsmart_dw_final.db' AS meu_disco;


DROP TABLE IF EXISTS meu_disco.fct_loads;
CREATE TABLE meu_disco.fct_loads AS SELECT * FROM fct_loads;

DROP TABLE IF EXISTS meu_disco.dim_lanes;
CREATE TABLE meu_disco.dim_lanes AS SELECT * FROM dim_lanes;
DROP TABLE IF EXISTS meu_disco.dim_shippers;
CREATE TABLE meu_disco.dim_shippers AS SELECT * FROM dim_shippers;
DROP TABLE IF EXISTS meu_disco.dim_carriers;
CREATE TABLE meu_disco.dim_carriers AS SELECT * FROM dim_carriers;

DROP TABLE IF EXISTS meu_disco.stg_loads;
CREATE TABLE meu_disco.stg_loads AS SELECT * FROM stg_loads;


DETACH meu_disco;