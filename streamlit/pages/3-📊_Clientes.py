import streamlit as st
import pandas as pd
import sys
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente de um arquivo .env
load_dotenv()
# Append the utils directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from helper_functions import get_data_from_mongo, plot_graphic_4, plot_graphic_5,plot_graphic_7, plot_graphic_8, check_authentication, logged_out_option

# Configure o layout da página para 'wide'
st.set_page_config(layout='wide')

check_authentication()
logged_out_option()

url = os.getenv('URL_DB')
db_name = "AnaHealth"
collection_name_dataset = "Dataset"

df = get_data_from_mongo(url, db_name, collection_name_dataset)

st.title("Vizualizações sobre os dados")

# Crie duas colunas
col1, col2 = st.columns(2)

# Plot gráficos nas colunas
with col1:
    plot_graphic_4(df)
    plot_graphic_5(df)

with col2:
    plot_graphic_7(df)
    plot_graphic_8(df)