import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.model_selection import train_test_split
from bson.objectid import ObjectId
import sys
import os


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

   # Removendo linhas com valores NaN
    df_dropped = df.dropna()

    # Dividindo em conjuntos de treinamento e teste
    X = df_dropped.drop(columns=['stay_time'])  
    y = df_dropped['stay_time']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test

def perform_clustering(X_train, X_test):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    kmeans = KMeans(n_clusters=8, random_state=42)
    X_train['cluster'] = kmeans.fit_predict(X_train_scaled)
    X_test['cluster'] = kmeans.predict(X_test_scaled)

    # Calcular métricas para ambos os conjuntos
    silhouette_train = silhouette_score(X_train, X_train['cluster'])
    silhouette_test = silhouette_score(X_test, X_test['cluster'])
    ari_train = adjusted_rand_score(y_train, X_train['cluster'])
    ari_test = adjusted_rand_score(y_test, X_test['cluster'])

    return X_train, X_test, silhouette_train, silhouette_test, ari_train, ari_test

def plot_results(data, title):
    sns.set_style("whitegrid")
    palette = sns.color_palette("husl", 8)

    plt.figure(figsize=(12, 8))
    sns.boxplot(x='cluster', y='stay_time', data=data, palette=palette)
    plt.title(title, fontsize=20)
    plt.xlabel('Cluster', fontsize=16)
    plt.ylabel('Tempo de Permanência', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    st.pyplot(plt)

st.title("Modelo Preditivo com Clustering")

if df is not None:
    X_train, X_test, y_train, y_test = process_data(df)

    X_train, X_test, silhouette_train, silhouette_test, ari_train, ari_test = perform_clustering(X_train, X_test)

    # Exibir métricas e gráficos
    st.write(f"Silhouette Score (Treinamento): {silhouette_train}")
    st.write(f"Silhouette Score (Teste): {silhouette_test}")
    st.write(f"Adjusted Rand Index (Treinamento): {ari_train}")
    st.write(f"Adjusted Rand Index (Teste): {ari_test}")

    plot_results(X_train, 'Distribuição do Tempo de Permanência por Cluster (Treinamento)')
    plot_results(X_test, 'Distribuição do Tempo de Permanência por Cluster (Teste)')