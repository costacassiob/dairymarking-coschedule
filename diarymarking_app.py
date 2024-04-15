import streamlit as st
from streamlit_gsheets import GSheetsConnection
import toml
from criar_seçao import criar_secao  # Importa a função criar_secao do arquivo criar_sessao.py
from entrar_seçao import entrar_secao  # Importa a função entrar_secao do arquivo entrar_sessao.py

# Carregar configurações do arquivo secrets.toml
#with open("secrets.toml", "r") as f:
#    toml_arq = toml.load(f)

config = st.secrets["connections"]["gsheets"]

# Painel lateral esquerdo
st.sidebar.header("Options")
opcao = st.sidebar.radio("Choose an option:", ("Create a new session - Criar uma seção nova", "Enter a section - Entrar em uma seção existente"))

# Conexão com o Google Sheets
gsheet_conn = GSheetsConnection("gsheets", **config)

# Carregar e exibir a planilha
df = gsheet_conn.read(spreadsheet=config["spreadsheet"], ttl=5)

# Exibindo conteúdo na parte principal da tela
st.write("Welcome to the data tagging system | Bem-vindo ao sistema de marcação de datas.")

# Se a opção selecionada for "Criar uma sessão nova", chama a função criar_secao
if opcao == "Create a new session - Criar uma seção nova":
    criar_secao(df,config)
# Se a opção selecionada for "Entrar em uma sessão existente", chama a função entrar_secao
elif opcao == "Enter a section - Entrar em uma seção existente":
    entrar_secao(df,config)

