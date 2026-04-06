import duckdb
import os

#caminhos
db_path = '/home/emile/Documentos/Analytics-Engineer-Challenge/data/loadsmart_dw_final.db'
output_dir = '/home/emile/Documentos/Analytics-Engineer-Challenge/data/'

conn = duckdb.connect(db_path, read_only=True)



try:
    data_fato = conn.execute("SELECT * FROM fct_loads").df()
    data_fato.to_csv(os.path.join(output_dir, 'gold_fct_loads.csv'),decimal=',', index=False)
    print('fato exportado')

    # B. Exportando Dimensão de Shippers (Clientes)
    data_shippers = conn.execute("SELECT * FROM dim_shippers").df()
    data_shippers.to_csv(os.path.join(output_dir, 'gold_dim_shippers.csv'), decimal=',',index=False)
    print('shippers exportada.')

    # C. Exportando Dimensão de Carriers (Transportadoras)
    data_carriers = conn.execute("SELECT * FROM dim_carriers").df()
    data_carriers.to_csv(os.path.join(output_dir, 'gold_dim_carriers.csv'), decimal=',', index=False)
    print('carriers exportada.')

    # D. Exportando Dimensão de Lanes (Rotas)
    data_lanes = conn.execute("SELECT * FROM dim_lanes").df()
    data_lanes.to_csv(os.path.join(output_dir, 'gold_dim_lanes.csv'), decimal=',', index=False)
    print('lanes exportada.')



except Exception as e:
    print('erro')

finally:
    conn.close()