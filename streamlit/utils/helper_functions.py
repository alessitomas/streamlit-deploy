import pandas as pd
from pymongo import MongoClient
from data_preprocessing import preprocessing
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go

def get_data_from_mongo(url ,db_name, collection_name):
    client = MongoClient(url)  
    db = client[db_name]
    collection = db[collection_name]
    data = pd.DataFrame(list(collection.find()))
    return data


def update_data_in_mongo(url ,db_name, collection_name, df):
    client = MongoClient(url)
    db = client[db_name]
    collection = db[collection_name]
    collection.delete_many({})
    preprocessed_df = preprocessing(df)
    data = preprocessed_df.to_dict("records")
    collection.insert_many(data)



def plot_graphic_1(df):
    df['PESSOA_PIPEDRIVE_contract_start_date'] = pd.to_datetime(df['PESSOA_PIPEDRIVE_contract_start_date'])
    df['PESSOA_PIPEDRIVE_contract_end_date'] = pd.to_datetime(df['PESSOA_PIPEDRIVE_contract_end_date'])

    df['Start_Month_Year'] = df['PESSOA_PIPEDRIVE_contract_start_date'].dt.to_period('M')
    df['End_Month_Year'] = df['PESSOA_PIPEDRIVE_contract_end_date'].dt.to_period('M')

    start_counts = df['Start_Month_Year'].value_counts().sort_index()
    end_counts = df['End_Month_Year'].value_counts().sort_index()


    fig = go.Figure()
    fig.add_trace(go.Bar(x=start_counts.index.astype(str), y=start_counts, name='Entradas'))
    fig.add_trace(go.Bar(x=end_counts.index.astype(str), y=end_counts, name='Saídas'))


    fig.update_layout(
        title='Histograma de Entrada e Saída de Assinaturas por Mês',
        xaxis_title='Ano e Mês',
        yaxis_title='Quantidade de Assinaturas',
        barmode='group'
    )

    # Display the figure in Streamlit
    st.plotly_chart(fig)