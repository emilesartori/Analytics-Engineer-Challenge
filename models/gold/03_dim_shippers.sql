/*
    DIMENSÃO: dim_shippers
    CAMADA: Gold
    DESCRIÇÃO: Cadastro clientes
    OBJETIVO: análise de clientes
*/

DROP TABLE IF EXISTS dim_shippers;

CREATE TABLE dim_shippers AS
SELECT
    -- id
    md5(shipper_name) as shipper_id,  

    shipper_name

FROM stg_loads

GROUP BY 1, 2;