import streamlit as st
import calendar
import json
from streamlit_gsheets import GSheetsConnection
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import toml
import datetime

def toggle_button_state(button_key, datas_selecionadas):
    datas_selecionadas = list(datas_selecionadas)
    if button_key in datas_selecionadas:
        datas_selecionadas.remove(button_key)
    else:
        datas_selecionadas.append(button_key)
    return datas_selecionadas

def entrar_secao(df,config):
    st.title("Select Dates")
    st.write('<html lang="pt-br"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><h2>Já Possui uma Seção?</h2><p>Se você já possui o código de uma seção, vá em "Entrar em uma seção existente" para escolher as datas em que está disponível.</p><p>Preencha o campo "Please inform the Section:" com o código da seção que você possui. Informe seu e-mail no campo "Please inform your email:", selecione o ano em "Year:" e o mês em "Month:".</p><p>Clique nas datas desejadas. Após selecionadas, clique em "Confirm". Pronto! Sua parte está feita. Agora é só aguardar o dono da seção gerar o relatório após todos escolherem as datas.</p></body></html>')

    Section = st.text_input("Please inform the Section:", key="section_input")
    Section_email = st.text_input("Please inform your email:", key="email_input")

    # Obtendo o ano e o mês atuais
    now = datetime.datetime.now()
    ano_padrao = now.year
    mes_padrao = now.month


    # Componentes de entrada com valores padrão
    ano = st.number_input("Year:", min_value=1900, max_value=2100, value=ano_padrao, key="ano_input")
    mes = st.selectbox("Month:", options=range(1, 13), format_func=lambda x: calendar.month_name[x], index=mes_padrao-1, key="mes_input")

    dias_do_mes = calendar.monthcalendar(ano, mes)

    datas_selecionadas = st.session_state.get('datas_selecionadas', [])

    # Mapeamento dos índices dos dias da semana para seus nomes
    dias_da_semana = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    with st.container():
        st.write("Semana:")
        # Adicionando o nome de cada dia da semana sobre as colunas correspondentes
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        for dia_idx, dia_da_semana in enumerate(dias_da_semana):
            with [col1, col2, col3, col4, col5, col6, col7][dia_idx]:
                st.button(label=dia_da_semana, key=f"day_of_week_{dia_idx}", disabled=True)
        
        # Variável para rastrear se já foi encontrado o primeiro dia da semana diferente de zero
        primeiro_dia_nao_zero_encontrado = False

        # Adicionando botões em colunas
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        for semana_idx, semana in enumerate(dias_do_mes):
            for dia_idx, dia in enumerate(semana):
                # Verifica se é o primeiro dia da semana diferente de zero
                if dia != 0 and not primeiro_dia_nao_zero_encontrado:
                    primeiro_dia_nao_zero_encontrado = True
                    # Preenche as colunas anteriores com botões com texto "X"
                    for i in range(dia_idx):
                        with [col1, col2, col3, col4, col5, col6, col7][i]:
                            st.button(label="X", key=f"empty_{semana_idx}_{i}", disabled=True)
                
                if dia != 0:
                    button_key = f"{ano}-{mes}-{semana_idx + 1}-{dia_idx}-{dia}"  # Chave única para o botão
                    if button_key in datas_selecionadas:
                        button_type = 'primary'
                    else:
                        button_type = 'secondary'
                    # Determinando a coluna correspondente ao dia da semana
                    col = [col1, col2, col3, col4, col5, col6, col7][dia_idx]
                    with col:
                        # Adiciona o botão do dia
                        if st.button(label=str(dia), key=button_key, help=f"Toggle button {button_key}", type=button_type):
                            datas_selecionadas = toggle_button_state(button_key, datas_selecionadas)
                            st.session_state['datas_selecionadas'] = datas_selecionadas
                            # Atualiza imediatamente a mudança de cor dos botões
                            st.experimental_rerun()

    # Exibe as datas selecionadas
    datas_selecionadas_str = []
    for data in datas_selecionadas:
        ano, mes, semana_idx, dia_idx, dia = map(int, data.split("-"))
        datas_selecionadas_str.append(f"{ano}/{mes}/{dia}")
    st.write("Dates:", ", ".join(datas_selecionadas_str))

    if st.button("Confirm"):

        if not Section or Section not in df["SEÇÃO"].values:
            st.error("Please enter a valid Section.")
        else:
            st.success("Your calendar has been successfully saved in Section {}".format(Section)) 
            # Autenticar e criar uma conexão com o Google Sheets
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(config, scope)
            client = gspread.authorize(credentials)

            # Abrir a planilha
            spreadsheet_key = "18TBuWJj7sbR1Ndbp97HXZiIHvSbEsAVKRAlp6gqytxo"
            worksheet_name = "DATAS"  # Substitua pelo nome da sua planilha
            worksheet = client.open_by_key(spreadsheet_key).worksheet(worksheet_name)

            # Adicionar uma nova linha
            nova_linha = [Section, Section_email, str(datas_selecionadas_str),"DISPONÍVEL"]  # Substitua pelos dados da sua nova linha
            worksheet.append_row(nova_linha)


