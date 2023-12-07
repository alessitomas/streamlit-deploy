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

check_authentication()
logged_out_option()

url = os.getenv('URL_DB')
db_name = "AnaHealth"
collection_name_dataset = "Dataset"


df = get_data_from_mongo(url, db_name, collection_name_dataset)

st.title("Vizualizações sobre os dados")


st.write("Entrada e saída de clientes a cada mês")

plot_graphic_4(df)
plot_graphic_7(df)
plot_graphic_5(df)
plot_graphic_8(df)