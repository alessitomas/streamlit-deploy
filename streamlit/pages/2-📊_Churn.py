import streamlit as st
import pandas as pd
import sys
import os

# Append the utils directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from helper_functions import get_data_from_mongo, plot_graphic_1, plot_graphic_2,plot_graphic_3,plot_graphic_6, plot_graphic_9, plot_graphic_10, check_authentication, logged_out_option

url = st.secrets.URL_DB
db_name = "AnaHealth"
collection_name_dataset = "Dataset"


df = get_data_from_mongo(url, db_name, collection_name_dataset)

st.title("Vizualizações sobre os dados")

# Add a multi-select box in the sidebar with all options selected by default
options = st.sidebar.multiselect(
    'Escolha os gráficos para comparar',
    ('Todos','Entrada e Saída de Assinaturas por Ano', 'Entrada e Saída de Assinaturas por Mês', 'Tendências de Churn por Mês', 'Motivos de Encerramento de Contrato de Assinatura', 'Tem Canal de Preferência', 'Tipo de contato preferido'),
    default=['Entrada e Saída de Assinaturas por Ano', 'Entrada e Saída de Assinaturas por Mês', 'Tendências de Churn por Mês', 'Motivos de Encerramento de Contrato de Assinatura', 'Tem Canal de Preferência', 'Tipo de contato preferido'])

check_authentication()
logged_out_option()

# Display the selected graphs
for option in options:
    if option == 'Todos':
        plot_graphic_1(df)
        plot_graphic_2(df)
        plot_graphic_3(df)
        plot_graphic_6(df)
        plot_graphic_9(df)
        plot_graphic_10(df)
    elif option == 'Entrada e Saída de Assinaturas por Ano':
        plot_graphic_10(df)
    elif option == 'Entrada e Saída de Assinaturas por Mês':
        plot_graphic_1(df)
    elif option == 'Tendências de Churn por Mês':
        plot_graphic_2(df)
    elif option == 'Motivos de Encerramento de Contrato de Assinatura':
        plot_graphic_3(df)
    elif option == 'Tem Canal de Preferência':
        plot_graphic_6(df)
    elif option == 'Tipo de contato preferido':
        plot_graphic_9(df)