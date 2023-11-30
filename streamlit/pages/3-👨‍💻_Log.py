from pymongo import MongoClient
import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
from helper_functions import get_logs, check_authentication, logged_out_option


check_authentication()
logged_out_option()

url = os.getenv('URL_DB')
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
        st.dataframe(logs_df)
    else:
        st.write("No logs found")

show_logs_page()