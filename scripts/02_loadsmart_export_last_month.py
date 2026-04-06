#pip install pysftp
#pip install paramiko==2.12.0


import duckdb
import pandas as pd
import smtplib
import pysftp
import os
from email.message import EmailMessage


#configuracao email
# FIZ O TESTE COM MEU EMAIL DO GMAIL, PARA OUTRO PROVEDOR DE E-MAIL, BASTA AJUSTAR AS CONFIGURAÇÕES DE SMTP.
#SMTP_SERVER = 'smtp.gmail.com'
#SMTP_PORT = 587
#EMAIL_USER = 'emilesartori@gmail.com'
#EMAIL_PASS = 'minhasenha'


#configuracao email
SMTP_SERVER = "INFORME O SERVIDOR SMTP"
SMTP_PORT = "INFORME A PORTA SMTP"
EMAIL_USER = "INFORME SEU EMAIL"
EMAIL_PASS = "INFORME SUA SENHA"



# FIZ O TESTE COM UM FTP LOCAL
#configuracao sftp
#SFTP_HOST = "127.0.0.1"
#SFTP_USER = "emile"
#SFTP_PASS = "1234"


#configuracao sftp
SFTP_HOST = "INFORME SEU FTP"
SFTP_USER = "INFORME SEU USUARIO"
SFTP_PASS = "INFORME SUA SENHA"



#arquivos - informe o arquivo a ser enviado e o sftp de destino
csv_origem = '/home/emile/Documentos/Analytics-Engineer-Challenge/data/export_loadsmart_last_month.csv'
diretorio_destino = '/home/emile/Documentos/teste_sftp_destino'


# --- FUNÇÕES SOLICITADAS ---

#ii. Enviar o arquivo CSV por e-mail para um destinatário específico.

def send_csv_via_email(file_path, subject, body, to_email):
    
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = to_email
    msg.set_content(body)

    # Anexando o arquivo
    with open(file_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(file_path)
        msg.add_attachment(file_data, maintype='application', subtype='csv', filename=file_name)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
    print('E-mail enviado com sucesso!')
    

#iii. Enviar o arquivo CSV para um servidor FTP/SFTP.    
def send_csv_via_sftp(csv_origem, diretorio_destino):
    
    
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None 
    
    with pysftp.Connection(SFTP_HOST, username=SFTP_USER, password=SFTP_PASS, cnopts=cnopts) as sftp:
        sftp.put(csv_origem, diretorio_destino)
    print('arquivo enviado para o FTP')





# CSV com dados do último mês

db_path = '/home/emile/Documentos/Analytics-Engineer-Challenge/data/loadsmart_dw_final.db'
conn = duckdb.connect(db_path, read_only=True)

try:
    query_export = """
    WITH referencia AS (
        SELECT date_trunc('month', max(delivery_at)) as mes_filtro
        FROM fct_loads
    )
    SELECT 
        f.loadsmart_id,
        s.shipper_name,
        f.delivery_at as delivery_date,
        l.pickup_city,
        l.pickup_state,
        l.delivery_city,
        l.delivery_state,
        f.book_price,
        c.carrier_name as Carrier_name
    FROM fct_loads f
    JOIN dim_shippers s ON f.shipper_id = s.shipper_id
    JOIN dim_carriers c ON f.carrier_id = c.carrier_id
    JOIN dim_lanes l    ON f.lane_id = l.lane_id
    WHERE date_trunc('month', f.delivery_at) = (SELECT mes_filtro FROM referencia)
    ORDER BY f.delivery_at DESC;
    """

    data_final = conn.execute(query_export).df()
    output_csv = '/home/emile/Documentos/Analytics-Engineer-Challenge/data/export_loadsmart_last_month.csv'
    data_final.to_csv(output_csv, index=False, encoding='utf-8')
    print('arquivo gerado')
except Exception as e:
    print('Erro ao gerar')

finally:
    conn.close()




# usando as funções

send_csv_via_email(output_csv, "Relatório de Entregas - Último Mês", "Segue anexo o arquivo solicitado.", "emilesartori@gmail.com")
print('E-mail enviado com sucesso!')
send_csv_via_sftp(csv_origem, diretorio_destino)
print('arquivo enviado para o FTP')

