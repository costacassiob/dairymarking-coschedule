import streamlit as st
from Sendemail import enviar_email  # Importa a função Sendemail do arquivo Sendemail.py
import random
from streamlit_gsheets import GSheetsConnection
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import toml
import pandas as pd
import re

def ler_datas_google_sheets(config,login_u):
    
    # Autenticar e criar uma conexão com o Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(config, scope)
    client = gspread.authorize(credentials)
    
    config2 = st.secrets["connections"]["web"]

    # Definir a expressão regular para extrair o ID da planilha
    pattern = r"/d/([a-zA-Z0-9-_]+)"

    # Aplicar a expressão regular na URL da planilha
    match = re.search(pattern, config2)
    spreadsheet_id = match.group(1)

    # Abrir a planilha
    spreadsheet_key = spreadsheet_id
    worksheet_name = "DATAS"  # Substitua pelo nome da sua planilha
    worksheet = client.open_by_key(spreadsheet_key).worksheet(worksheet_name)

    dados = worksheet.get_all_values()

    # Transformar os dados em um DataFrame do Pandas
    data_frame = pd.DataFrame(dados[1:], columns=dados[0])

    df_filtrado = data_frame[data_frame['SEÇÃO'] == login_u]

    # Concatenar todas as listas de datas em uma única lista
    datas_secao = []
    for datas_lista in df_filtrado['DATA']:
        datas_secao.extend(datas_lista)

    # Criar um dicionário para contar a frequência das datas
    frequencia_datas = {}

    # Contar a frequência de cada data na lista datas_secao
    for data in datas_secao:
        if data in frequencia_datas:
            frequencia_datas[data] += 1
        else:
            frequencia_datas[data] = 1

    # Ordenar o dicionário pelas contagens em ordem decrescente
    frequencia_datas_ordenado = sorted(frequencia_datas.items(), key=lambda x: x[1], reverse=True)

    # Exibir as datas com a contagem ao lado
    print("Datas com maior frequência:")
    for data, frequencia in frequencia_datas_ordenado:
        st.write(f"{data}: {frequencia}")
