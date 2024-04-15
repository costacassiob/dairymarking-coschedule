import streamlit as st
from Sendemail import enviar_email  # Importa a função Sendemail do arquivo Sendemail.py
import random
from streamlit_gsheets import GSheetsConnection
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from Verificação_datas import ler_datas_google_sheets
import toml

def criar_secao(df,config):
    
    # Adicione aqui a lógica para criar uma nova sessão
    destinatario = st.text_input("Enter your email:")
    if st.button("Confirm"):

        # Função para validar o formato do email
        def validar_email(email):
            # Verifica se o email tem um @ e pelo menos um ponto depois do @
            return "@" in email and "." in email[email.index("@"):]

        if not destinatario or not validar_email(destinatario):
            st.error("Please enter a valid email.")
        else:
            # Chama a função enviar_email para enviar o e-mail, passando o email fornecido como argumento.
            login_usu, senha_usu = gerar_login(df,destinatario,config)
            password = st.secrets["connections"]["web"]["password"]
            enviar_email(destinatario, login_usu, senha_usu,password)  # Aqui você pode passar os argumentos necessários, se houver

            st.success("An email with Section and Password has been successfully sent to {}. | A Seção e a senha foram enviados com sucesso para o email {}".format(destinatario, destinatario))


    st.write("Enter your section and password to view a report of available dates for your group.| Informe sua seção e senha para gerar relatório de datas disponíveis do seu grupo.")

    login_u = st.text_input("Enter your Section:")
    senha_u = st.text_input("Enter your Password:")
    if st.button("View report - Gerar relatório"):
  
        if login_u in df["SEÇÃO"].values:
            senha_correspondente = df.loc[df["SEÇÃO"] == login_u, "SENHA"].values[0]
            if senha_u == senha_correspondente:
                st.success("Wait for file to be generated - date formatted YYYY/MM/DD")
                ler_datas_google_sheets(config,login_u)
            else:
                st.error("Incorrect Section or Password")
        else:
            st.error("Incorrect Section or Password")


def gerar_login(df,destinatario,config):

    senha_usu = ""
    login_usu = ""

    caracteresLetra = "abcdefghijklmnopqrstuvxz"
    caracteresLetraMaiuscula = "QWERTYUIOIPASDFGHJKLÇZXCVBNM"
    caracteresNumero = "0123456789"
    caracteresEspecial = "!@#$%&*?*"

    for digito in range (2):
        aleatorio1 = random.choice(caracteresLetraMaiuscula)
        senha_usu += aleatorio1
    for digito in range (2):
        aleatorio1 = random.choice(caracteresLetra)
        senha_usu += aleatorio1
    for digito in range (2):
        aleatorio2 = random.choice(caracteresEspecial)
        senha_usu += aleatorio2
    for digito in range (2):
        aleatorio3 = random.choice(caracteresNumero)
        senha_usu += aleatorio3

    for digito in range (5):
        aleatorio1 = random.choice(caracteresNumero)
        login_usu += aleatorio1
    for digito in range (1):
        aleatorio1 = random.choice(caracteresLetraMaiuscula)
        login_usu += aleatorio1
    for digito in range (5):
        aleatorio1 = random.choice(caracteresNumero)
        login_usu += aleatorio1
    for digito in range (1):
        aleatorio1 = random.choice(caracteresLetraMaiuscula)
        login_usu += aleatorio1
    
    if login_usu in df["SEÇÃO"].values:
        gerar_login(df)
    else:
        
        # Autenticar e criar uma conexão com o Google Sheets
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(config, scope)
        client = gspread.authorize(credentials)

        # Abrir a planilha
        spreadsheet_key = "18TBuWJj7sbR1Ndbp97HXZiIHvSbEsAVKRAlp6gqytxo"
        print(spreadsheet_key)
        worksheet_name = "SECAO"  # Substitua pelo nome da sua planilha
        worksheet = client.open_by_key(spreadsheet_key).worksheet(worksheet_name)

        # Adicionar uma nova linha
        nova_linha = [login_usu, senha_usu, destinatario]  # Substitua pelos dados da sua nova linha
        worksheet.append_row(nova_linha)

    return login_usu, senha_usu
                    
