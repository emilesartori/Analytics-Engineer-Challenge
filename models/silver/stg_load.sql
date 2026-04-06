/*
    MODELO: stg_loads
    CAMADA: Silver
    DESCRIÇÃO: limpeza e padronização dos dados.
    OBJETIVO: criação stage
*/

DROP VIEW IF EXISTS stg_loads;

CREATE VIEW stg_loads AS
SELECT
    loadsmart_id,
    
    -- cidade e estado
    upper(trim(coalesce(pickup_city, 'N/A'))) as pickup_city,
    upper(trim(coalesce(pickup_state, 'N/A'))) as pickup_state,
    upper(trim(coalesce(delivery_city, 'N/A'))) as delivery_city,
    upper(trim(coalesce(delivery_state, 'N/A'))) as delivery_state,
    
    -- data 
    cast(quote_date as timestamp) as quote_at,
    cast(book_date as timestamp) as book_at,
    cast(delivery_date as timestamp) as delivery_at,
    
    -- valores 
    cast(coalesce(book_price, 0) as decimal(18,2)) as book_price,
    cast(coalesce(source_price, 0) as decimal(18,2)) as source_price,
    cast(coalesce(pnl, 0) as decimal(18,2)) as pnl,
    cast(coalesce(mileage, 0) as float) as mileage,
    
    -- entidades 
    upper(trim(coalesce(shipper_name, 'UNKNOWN'))) as shipper_name,
    upper(trim(coalesce(carrier_name, 'UNKNOWN'))) as carrier_name,
    
    -- booleanos 
    cast(coalesce(has_mobile_app_tracking, false) as boolean) as has_mobile_tracking,
    cast(coalesce(load_was_cancelled, false) as boolean) as is_cancelled,
    cast(coalesce(has_macropoint_tracking, false) as boolean) as has_macropoint_tracking,
    cast(coalesce(has_edi_tracking, false) as boolean) as has_edi_tracking
    
FROM raw_loads;

