import duckdb
import pandas as pd

# banco
db_path = '/home/emile/Documentos/Analytics-Engineer-Challenge/data/loadsmart_dw_final.db'

conn = duckdb.connect(db_path, read_only=True)


try:
    #selecionando colunas
    query_full_export = """
    SELECT 
        f.loadsmart_id,
        s.shipper_name,
        f.delivery_at as delivery_date,
        l.pickup_city,
        l.pickup_state,
        l.delivery_city,
        l.delivery_state,
        f.book_price,
        f.source_price,
        f.pnl,
        f.mileage,
        c.carrier_name as Carrier_name,
        c.has_mobile_tracking
    FROM fct_loads f
    JOIN dim_shippers s ON f.shipper_id = s.shipper_id
    JOIN dim_carriers c ON f.carrier_id = c.carrier_id
    JOIN dim_lanes l    ON f.lane_id = l.lane_id
    ORDER BY f.delivery_at DESC;
    """

    #gerando csv completo
    data_full = conn.execute(query_full_export).df()
    
    output_csv = '/home/emile/Documentos/Analytics-Engineer-Challenge/data/export_loadsmart_FULL_dataset.csv'
    data_full.to_csv(output_csv, index=False, encoding='utf-8')

    print('arquivo gerado')
except Exception as e:
    print('erro ao gerar arquivo')

finally:
    conn.close()