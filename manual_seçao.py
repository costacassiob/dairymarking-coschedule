import streamlit as st
from Sendemail import enviar_email  # Importa a função Sendemail do arquivo Sendemail.py
import random
from streamlit_gsheets import GSheetsConnection
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from Verificação_datas import ler_datas_google_sheets
import toml

def manual_secao(df,config):
    st.write('<html lang="pt-br"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body><h2>Criar uma Seção:</h2><small><p>Para criar uma nova seção, vá em "Criar uma seção nova". Insira seu e-mail na opção "Enter your email:" e clique em confirmar para receber o código da seção e a senha.</p><p>Compartilhe o código da seção com as pessoas que deseja para que elas possam escolher as datas disponíveis.</small></p></body></html>', unsafe_allow_html=True)
    st.write('<html lang="pt-br"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><h2>Já Possui uma Seção?</h2><p>Se você já possui o código de uma seção, vá em "Entrar em uma seção existente" para escolher as datas em que está disponível.</p><p>Preencha o campo "Please inform the Section:" com o código da seção que você possui. Informe seu e-mail no campo "Please inform your email:", selecione o ano em "Year:" e o mês em "Month:".</p><p>Clique nas datas desejadas. Após selecionadas, clique em "Confirm". Pronto! Sua parte está feita. Agora é só aguardar o dono da seção gerar o relatório após todos escolherem as datas.</p></body></html>', unsafe_allow_html=True)
    
                    
