import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def ler_datas_google_sheets(config, login_u):
    
    # Autenticar e criar uma conexão com o Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(config, scope)
    client = gspread.authorize(credentials)
    
    # Abrir a planilha
    spreadsheet_key = config["spreadsheet"].split("/d/")[1].split("/")[0]
    worksheet_name = "DATAS"  # Substitua pelo nome da sua planilha
    worksheet = client.open_by_key(spreadsheet_key).worksheet(worksheet_name)

    # Obter os dados do Google Sheets
    dados = worksheet.get_all_values()

    # Transformar os dados em um DataFrame do Pandas
    data_frame = pd.DataFrame(dados[1:], columns=dados[0])

    # Filtrar os dados pela seção do usuário
    df_filtrado = data_frame[data_frame['SEÇÃO'] == login_u]

    # Lista para armazenar todas as datas
    todas_datas = []

    # Percorre os dados filtrados
    for _, linha in df_filtrado.iterrows():
        # Extrai a lista de datas da coluna desejada (supondo que as datas estejam separadas por vírgula)
        datas_str = linha[2]
        # Remover os caracteres ' [ e ] e dividir a string em uma lista de datas
        datas_lista = datas_str.replace("'", "").replace("[", "").replace("]", "").split(',')
        # Adiciona as datas à lista geral
        todas_datas.extend(datas_lista)

    # Criar DataFrame com as datas
    df_f = pd.DataFrame(todas_datas, columns=['Data'])

    # Contagem de frequência das datas e ordenação
    contagem_datas = df_f['Data'].value_counts().reset_index()
    contagem_datas.columns = ['Data', 'Frequência']
    contagem_datas = contagem_datas.sort_values(by='Frequência', ascending=False)

    st.write(contagem_datas)

