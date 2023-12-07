import streamlit as st
import pandas as pd
import sys
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente de um arquivo .env
load_dotenv()
# Append the utils directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from helper_functions import get_data_from_mongo, plot_graphic_1, plot_graphic_2,plot_graphic_3,plot_graphic_6, plot_graphic_9, plot_graphic_10, check_authentication, logged_out_option

check_authentication()
logged_out_option()

url = os.getenv('URL_DB')
db_name = "AnaHealth"
collection_name_dataset = "Dataset"


df = get_data_from_mongo(url, db_name, collection_name_dataset)

st.title("Vizualizações sobre os dados")


st.write("Entrada e saída de clientes a cada mês")

plot_graphic_10(df)
plot_graphic_1(df)
plot_graphic_2(df)
plot_graphic_3(df)
plot_graphic_6(df)
plot_graphic_9(df)
