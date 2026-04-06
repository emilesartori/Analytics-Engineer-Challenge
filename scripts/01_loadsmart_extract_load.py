# -*- coding: utf-8 -*-
#Loadsmart- analytics engineer

# emile 2026-04-02



# pip install pandas duckdb

import pandas as pd
import duckdb
import os

#altere o diretório do arquivo a ser importado:
path = r'/home/emile/Documentos/Analytics-Engineer-Challenge/data'


#csv original:
filename = '2026_data_challenge_ae_data.csv'


#lendo arquivo
data = pd.read_csv(os.path.join(path, filename))


#explorando os dados
print(data.describe())
print(data.info())
print(data.head())


# Colunas que não devem ser convertidas
exclude_from_date = [
    'carrier_on_time_to_pickup',
    'carrier_on_time_to_delivery',
    'carrier_on_time_overall',
    'has_mobile_app_tracking',
    'has_macropoint_tracking',
    'has_edi_tracking'
]

# Identificando colunas de data automaticamente
date_cols = [c for c in data.columns if any(x in c for x in ['date', 'time', 'appointment'])]

for col in date_cols:
    if col not in exclude_from_date and data[col].dtype == 'object':
        data[col] = pd.to_datetime(data[col], errors='raise')


#convertendo numeros
numeric_cols = ['book_price', 'source_price', 'pnl', 'mileage']
for col in numeric_cols:
    data[col] = pd.to_numeric(data[col], errors='raise')



# função para separar as colunas:
def split_lane_details(lane_string):

    if pd.isna(lane_string):
        return pd.Series([None, None, None, None])
    
    try:
        # limpas ' e espaços
        clean_lane = lane_string.replace('"', '').strip()
        
        # divide na seta '->'
        if ' -> ' in clean_lane:
            origin_part, dest_part = clean_lane.split(' -> ')
        else:
            return pd.Series([None, None, None, None])

        #separa cidade e estado
        def extract_geography(part):
            parts = [p.strip() for p in part.rsplit(',', 1)]
            return parts if len(parts) == 2 else [part, None]

        pickup_city, pickup_state = extract_geography(origin_part)
        delivery_city, delivery_state = extract_geography(dest_part)
        
        return pd.Series([pickup_city, pickup_state, delivery_city, delivery_state])
    
    except Exception as e:
        return pd.Series([None, None, None, None])
    

# Aplicando a função 
data[['pickup_city', 'pickup_state', 'delivery_city', 'delivery_state']] = data['lane'].apply(split_lane_details)


#criando banco
db_filename = os.path.join(path, "loadsmart_dw_raw.db")

# Remove o banco antigo se existir 
if os.path.exists(db_filename):
    os.remove(db_filename)

print(f"\Criando banco: {db_filename}")
con = duckdb.connect(db_filename)

# Criando a tabela 'raw_loads' 
con.execute("CREATE TABLE raw_loads AS SELECT * FROM data")

# Validação final da carga
row_count = con.execute("SELECT count(*) FROM raw_loads").fetchone()[0]


print(f"Total de linhas incluídas: {row_count}")


con.close()