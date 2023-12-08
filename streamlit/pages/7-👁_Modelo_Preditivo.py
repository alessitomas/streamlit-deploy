import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import silhouette_score, adjusted_rand_score
from bson.objectid import ObjectId
import sys
import os
from sklearn.model_selection import train_test_split



# Append the utils directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from helper_functions import get_data_from_mongo,check_authentication, logged_out_option
url = st.secrets['URL_DB']
db_name = "AnaHealth"
collection_name_dataset = "Dataset"

df = get_data_from_mongo(url, db_name, collection_name_dataset)

check_authentication()
logged_out_option()


def process_data(df):
    # Convertendo ObjectId para string
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].apply(lambda x: str(x) if isinstance(x, ObjectId) else x)


    # Criando a coluna 'stay_time'
    tempo_permanencia = []
    for indice, valor in df["FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"].items():
        if pd.notna(valor):
            index = valor.find(";")
            if index != -1:
                valor = valor[:index]
            df.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"] = valor

    for indice, valor in df["FUNIL_ASSINATURA_PIPEDRIVE_lost_time"].items():
        if pd.notna(df.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"]):
            tempo_1 = datetime.strptime(valor, '%Y-%m-%d')
            tempo_2 = datetime.strptime(df.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"], '%Y-%m-%d')
        else:
            tempo_1 = datetime.strptime(valor, '%Y-%m-%d')
            tempo_2 = datetime.strptime(df.loc[indice, "PESSOA_PIPEDRIVE_contract_start_date"], '%Y-%m-%d')
        tempo_permanencia.append(str(tempo_1 - tempo_2))

    df['stay_time'] = tempo_permanencia
    for indice, valor in df["stay_time"].items():
        index = valor.find(",")
        if index != -1:
            valor = valor[:index]
        df.loc[indice, "stay_time"] = valor

    df["stay_time"] = df["stay_time"].str.extract('(\d+)').astype(float)
    df["stay_time"] = np.nan_to_num(df["stay_time"], nan=0)

    cols_to_remove = ["PESSOA_PIPEDRIVE_id_person", "PESSOA_PIPEDRIVE_id_gender"]
    df.drop(columns=cols_to_remove, inplace=True)

    # Verificar e converter tipos de dados
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_numeric(df[col])
            except ValueError:
                df.drop(col, axis=1, inplace=True)  # Remover a coluna se não puder ser convertida

   
    # Preencher valores NaN com 0
    df.fillna(0, inplace=True)

    return df


# Função para realizar o clustering
def perform_clustering(data):
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)

    kmeans = KMeans(n_clusters=8, random_state=42)
    data['cluster'] = kmeans.fit_predict(data)

    # Calcular métricas
    silhouette = silhouette_score(data, data['cluster'])
    ari = adjusted_rand_score(data['stay_time'], data['cluster'])
    return data, silhouette, ari

# Função para plotar os resultados
    # Função para plotar os resultados
def plot_results(data):
    # Definir o estilo do Seaborn
    sns.set_style("whitegrid")

    # Criar uma paleta de cores
    palette = sns.color_palette("husl", 8)

    plt.figure(figsize=(12, 8))
    sns.boxplot(x='cluster', y='stay_time', data=data, palette=palette)
    plt.title('Tempo de Permanência por Cluster', fontsize=18)
    plt.xlabel('Cluster', fontsize=16)
    plt.ylabel('Tempo de Permanência', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    st.pyplot(plt)


# Interface do Streamlit
st.title("Modelo Preditivo com Clustering")


if df is not None:
    processed_data = process_data(df)  # Use a função process_data

    # Executar clustering
    clustered_data, silhouette, ari = perform_clustering(processed_data)

    # Exibir métricas e gráficos
    st.write(f"Silhouette Score: {silhouette}")
    st.write(f"Adjusted Rand Index: {ari}")
    plot_results(clustered_data)