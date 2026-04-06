/*
    TABELA FATO: fct_loads
    CAMADA: Gold
    DESCRIÇÃO: transações
    OBJETIVO: análise de transações    
*/

DROP TABLE IF EXISTS fct_loads;

CREATE TABLE fct_loads AS
SELECT
    -- id
    loadsmart_id,
   
    md5(concat(pickup_city, pickup_state, delivery_city, delivery_state)) as lane_id,
    md5(shipper_name) as shipper_id,
    md5(carrier_name) as carrier_id,
    
    -- data
    delivery_at,
    
    -- valores
    book_price,    -- preço pago pelo Shipper
    source_price,  -- preço pago para a transportadora
    pnl,           -- lucro/prejuizo
    mileage,        -- distância

    -- flags
    has_mobile_tracking,
    has_macropoint_tracking,
    has_edi_tracking


FROM stg_loads
--filtrando apenas o que não foi cancelado.
WHERE is_cancelled = false;

