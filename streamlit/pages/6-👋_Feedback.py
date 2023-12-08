import streamlit as st
import pandas as pd
import sys
import os
import datetime

# Carregar variáveis de ambiente de um arquivo .env
# Append the utils directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from helper_functions import get_data_from_mongo, check_authentication, logged_out_option


check_authentication()
logged_out_option()

url = st.secrets['URL_DB']
db_name = "AnaHealth"
collection_name_dataset = "Dataset"

df = get_data_from_mongo(url, db_name, collection_name_dataset)

st.title("Página de Feedback")

# Coletar feedback do usuário
feedback = st.text_area("Por favor, deixe seu feedback aqui...")

# Coletar o nome do usuário (opcional)
name = st.text_input("Seu nome")

# Botão de envio
if st.button("Enviar Feedback"):
    # Aqui você pode escrever o código para salvar o feedback em um banco de dados ou arquivo
    with open('feedback.txt', 'a') as f:
        f.write(f'Feedback de {name}: {feedback}\n')

    st.success("Obrigado pelo seu feedback!")





        