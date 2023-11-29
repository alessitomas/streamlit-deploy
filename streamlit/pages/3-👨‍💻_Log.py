from pymongo import MongoClient
import streamlit as st

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from helper_functions import get_logs

url = os.getenv('MEU_SEGREDO_URL')
db_name = os.getenv('MEU_SEGREDO_DB_NAME')
collection_name = os.getenv('MEU_SEGREDO_COLLECTION_NAME_DATASET')

def show_logs_page():
    st.title("Log de Uso da Dashboard")
    logs = get_logs(url, db_name, collection_name)
    for user, action in logs:
        st.text(f"Usuário: {user} - Ação: {action}")

show_logs_page()
