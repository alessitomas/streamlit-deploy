from pymongo import MongoClient
import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
from helper_functions import get_logs, check_authentication, logged_out_option


check_authentication()
logged_out_option()

url = st.secrets.URL_DB
db_name = "AnaHealth"
collection_name_log = "Log"


def show_logs_page():
    st.title("Log de Uso da Dashboard")
    search_query = st.sidebar.text_input("Search logs")
    logs = get_logs(url, db_name, collection_name_log)
    if search_query:
        logs = [log for log in logs if search_query.lower() in str(log).lower()]
    if logs:
        logs_df = pd.DataFrame(logs, columns=['User', 'Action', 'Timestamp'])
        
        # Número de linhas e páginas
        rows_per_page = 10
        num_pages = len(logs_df) // rows_per_page
        if len(logs_df) % rows_per_page > 0:
            num_pages += 1

        # Usar um seletor numérico para selecionar a página
        page_num = st.number_input('Selecione a página', min_value=1, max_value=num_pages, value=1, step=1)

        # Exibir a página selecionada
        start_index = rows_per_page * (page_num - 1)
        end_index = start_index + rows_per_page
        st.table(logs_df[start_index:end_index])
    else:
        st.write("No logs found")

show_logs_page()