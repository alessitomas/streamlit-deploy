import streamlit as st
import pandas as pd
from pymongo import MongoClient
import sys
import os


# Append the utils directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from helper_functions import update_data_in_mongo, get_data_from_mongo, check_authentication, logged_out_option



check_authentication()
logged_out_option()

st.title('Upload de um arquivo CSV')
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv", help='Dataset em formato de arquivo CSV, será usado para as vizualizações.')

if uploaded_file is not None:
    
    df = pd.read_csv(uploaded_file)
    url = st.secrets.URL_DB
    db_name = "AnaHealth"
    collection_name = "Dataset"

    
    update_data_in_mongo(url, db_name, collection_name, df)
    new_df = get_data_from_mongo(url, db_name, collection_name)

    st.write(new_df)
    # Display success message
    st.success("Dados preprocessados e importados com sucesso para o MongoDB Atlas!")   
