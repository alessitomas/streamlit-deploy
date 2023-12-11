import streamlit as st
import pandas as pd
import sys
import os



# Append the utils directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from helper_functions import get_data_from_mongo, plot_graphic_4, plot_graphic_5,plot_graphic_7, plot_graphic_8, check_authentication, logged_out_option

url = st.secrets.URL_DB
db_name = "AnaHealth"
collection_name_dataset = "Dataset"

df = get_data_from_mongo(url, db_name, collection_name_dataset)

st.title("Vizualizações sobre os dados")

# Adicionar uma barra lateral
options = st.sidebar.multiselect(
    'Escolha os gráficos para comparar',
    ('Todos','Idade das Pessoas que Encerraram Contrato', 'Estados em que os clientes vivem', 'Cidades em que os clientes vivem','Gênero dos clientes'),
    default=['Idade das Pessoas que Encerraram Contrato', 'Estados em que os clientes vivem', 'Cidades em que os clientes vivem','Gênero dos clientes'])
    


check_authentication()
logged_out_option()

for option in options:
    if option == 'Todos':
        plot_graphic_4(df)
        plot_graphic_7(df)
        plot_graphic_5(df)
        plot_graphic_8(df)
    elif option == 'Idade das Pessoas que Encerraram Contrato':
        plot_graphic_4(df)
    elif option == 'Estados em que os clientes vivem':
        plot_graphic_7(df)
    elif option == 'Cidades em que os clientes vivem':
        plot_graphic_5(df)
    elif option == 'Gênero dos clientes':
        plot_graphic_8(df)
