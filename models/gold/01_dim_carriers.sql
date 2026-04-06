/*
    DIMENSÃO: dim_carriers
    CAMADA: Gold
    DESCRIÇÃO: transportadoras
    OBJETIVO: análise por transportadora

*/

DROP TABLE IF EXISTS dim_carriers;

CREATE TABLE dim_carriers AS
SELECT
    -- id
    md5(carrier_name) as carrier_id,
    carrier_name,    
    max(has_mobile_tracking) as has_mobile_tracking

FROM stg_loads
GROUP BY 1, 2;