import streamlit as st
import pandas as pd
from pymongo import MongoClient
import sys
import os

from dotenv import load_dotenv

# Carregar variáveis de ambiente de um arquivo .env
load_dotenv()
# Append the utils directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from helper_functions import update_data_in_mongo, get_data_from_mongo

st.title('Upload de um arquivo CSV')
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv", help='Dataset em formato de arquivo CSV, será usado para as vizualizações.')

if uploaded_file is not None:
    
    df = pd.read_csv(uploaded_file)
    url = os.getenv('MEU_SEGREDO_URL')
    db_name = os.getenv('MEU_SEGREDO_DB_NAME')
    collection_name = os.getenv('MEU_SEGREDO_COLLECTION_NAME')
    
    update_data_in_mongo(url, db_name, collection_name, df)
    new_df = get_data_from_mongo(url, db_name, collection_name)

    st.write(new_df)
    # Display success message
    st.success("Dados preprocessados e importados com sucesso para o MongoDB Atlas!")   
