/*
    DIMENSÃO: dim_lanes
    CAMADA: Gold
    DESCRIÇÃO: rotas
    OBJETIVO: análise de rotas
*/


DROP TABLE IF EXISTS dim_lanes;

CREATE TABLE dim_lanes AS
SELECT
    --criacao id
    md5(concat(pickup_city, pickup_state, delivery_city, delivery_state)) as lane_id,
    pickup_city,
    pickup_state,
    delivery_city,
    delivery_state
FROM stg_loads

GROUP BY 1, 2, 3, 4, 5;