SELECT 
    f.loadsmart_id,
    s.shipper_name as cliente,
    c.carrier_name as transportadora,
    l.pickup_city || ' -> ' || l.delivery_city as rota,
    f.pnl as lucro_liquido
FROM fct_loads f
JOIN dim_shippers s ON f.shipper_id = s.shipper_id
JOIN dim_carriers c ON f.carrier_id = c.carrier_id
JOIN dim_lanes l    ON f.lane_id = l.lane_id
ORDER BY f.pnl DESC
LIMIT 10;