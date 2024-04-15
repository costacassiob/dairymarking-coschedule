import streamlit as st
from streamlit_gsheets import GSheetsConnection
import toml
from criar_seçao import criar_secao  # Importa a função criar_secao do arquivo criar_sessao.py
from entrar_seçao import entrar_secao  # Importa a função entrar_secao do arquivo entrar_sessao.py

# Carregar configurações do arquivo secrets.toml
#with open("secrets.toml", "r") as f:
#    toml_arq = toml.load(f)

config = st.secrets["connections"]["gsheets"]

# Centralizar texto com borda no painel lateral
st.sidebar.markdown("""
    <style>
    .text-container {
        display: flex;
        justify-content: center;
    }
    .bordered-text {
        border: 2px solid #000080; /* Cor da borda (azul marinho) */
        padding: 10px; /* Espaçamento interno da borda */
        color: #000080; /* Cor do texto (azul marinho) */
        font-weight: bold; /* Negrito */
        font-size: x-large; /* Tamanho da fonte maior */
    }
    </style>
""", unsafe_allow_html=True)

# Incluir texto com borda no painel lateral
st.sidebar.markdown('<div class="text-container"><div class="bordered-text">CoSchedule</div></div>', unsafe_allow_html=True)

# Painel lateral esquerdo
st.sidebar.header("Options")
opcao = st.sidebar.radio("Choose an option:", ("Create a new session - Criar uma seção nova", "Enter a section - Entrar em uma seção existente"))

st.sidebar.write('<span style="color:green">Did you like my work? How about making a donation!?   |   Gostou do meu trabalho? Que tal fazer uma doação!?</span>', unsafe_allow_html=True)
st.sidebar.write('PIX: costa.bcassio@gmail.com', unsafe_allow_html=True)


# Inserir imagem centralizada no painel lateral
st.sidebar.image("QR-code.png", use_column_width=True, caption="Legenda da imagem")

# Aplicar estilo CSS para centralizar a imagem
st.markdown(
    """
    <style>
    .sidebar .stImage > div {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Conexão com o Google Sheets
gsheet_conn = GSheetsConnection("gsheets", **config)

# Carregar e exibir a planilha
df = gsheet_conn.read(spreadsheet=config["spreadsheet"], ttl=5)

st.write('<span style="color:red">OPEN ON COMPUTER   |   ABRA PELO COMPUTADOR</span>'
         , unsafe_allow_html=True)
st.write('<span style="color:red">OPEN ON COMPUTER   |   ABRA PELO COMPUTADOR</span>'
         , unsafe_allow_html=True)

# Exibindo conteúdo na parte principal da tela
st.write("Welcome to CoSchedule, the data tagging system | Bem-vindo ao CoSchedule, sistema de marcação de datas.")



st.write('<html lang="pt-br"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body><h2>Criar uma Seção:</h2><small><p>Para criar uma nova seção, vá em "Criar uma seção nova". Insira seu e-mail na opção "Enter your email:" e clique em confirmar para receber o código da seção e a senha.</p><p>Compartilhe o código da seção com as pessoas que deseja para que elas possam escolher as datas disponíveis.</small></p></body></html>', unsafe_allow_html=True)


# Se a opção selecionada for "Criar uma sessão nova", chama a função criar_secao
if opcao == "Create a new session - Criar uma seção nova":
    criar_secao(df,config)
# Se a opção selecionada for "Entrar em uma sessão existente", chama a função entrar_secao
elif opcao == "Enter a section - Entrar em uma seção existente":
    entrar_secao(df,config)

