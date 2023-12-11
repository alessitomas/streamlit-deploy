from tkinter import font
import pandas as pd
from datetime import datetime 
import numpy as np
from sklearn.discriminant_analysis import StandardScaler
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator, DataGenerator as dg
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.decomposition import PCA
import sys
import os
import streamlit as st


# Append the utils directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
sns.set(style="whitegrid")  # Set style to 'whitegrid' for better visibility

from helper_functions import get_data_from_mongo,check_authentication, logged_out_option

url = st.secrets['URL_DB']
db_name = "AnaHealth"
collection_name_dataset = "Dataset"

data = get_data_from_mongo(url, db_name, collection_name_dataset)

check_authentication()
logged_out_option()

# Interface do Streamlit
st.title("Modelo Preditivo com Clustering")

tempo_permanencia = []

for indice, valor in data["FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"].items():
    if pd.notna(valor):
        index = data.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"].find(";")
        if index != -1:
            data.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"] = data.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"][:index]

for indice, valor in data["FUNIL_ASSINATURA_PIPEDRIVE_lost_time"].items():
    if pd.notna(data.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"]):
        tempo_1 = datetime.strptime(data.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"], '%Y-%m-%d')
        tempo_2 = datetime.strptime(data.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"], '%Y-%m-%d')
        tempo_permanencia.append(str(tempo_1 - tempo_2))
    else:
        tempo_1 = datetime.strptime(data.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"], '%Y-%m-%d')
        tempo_2 = datetime.strptime(data.loc[indice, "PESSOA_PIPEDRIVE_contract_start_date"], '%Y-%m-%d')
        tempo_permanencia.append(str(tempo_1 - tempo_2))

data['stay_time'] = tempo_permanencia

for indice, valor in data["stay_time"].items():
    index = data.loc[indice, "stay_time"].find(",")
    if index != -1:
        data.loc[indice, "stay_time"] = data.loc[indice, "stay_time"][:index]

data["stay_time"] = data["stay_time"].str.extract('(\d+) days').astype(float)
data["stay_time"] = np.nan_to_num(data["stay_time"], nan=0)

data.drop(columns=["PESSOA_PIPEDRIVE_id_person", "PESSOA_PIPEDRIVE_id_gender","PESSOA_PIPEDRIVE_id_marrital_status","PESSOA_PIPEDRIVE_state", 
                   "PESSOA_PIPEDRIVE_city","PESSOA_PIPEDRIVE_postal_code","PESSOA_PIPEDRIVE_contract_start_date","PESSOA_PIPEDRIVE_contract_end_date",
                   "PESSOA_PIPEDRIVE_Canal de Preferência","FUNIL_ASSINATURA_PIPEDRIVE_id_stage","FUNIL_ASSINATURA_PIPEDRIVE_id_org", "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service","FUNIL_ASSINATURA_PIPEDRIVE_lost_time",
                    "FUNIL_ONBOARDING_PIPEDRIVE_add_time","FUNIL_ONBOARDING_PIPEDRIVE_status","FUNIL_ONBOARDING_PIPEDRIVE_lost_reason", "FUNIL_ONBOARDING_PIPEDRIVE_activities_count",
                     "ATENDIMENTOS_AGENDA_Datas Atendimento Médico", "ATENDIMENTOS_AGENDA_Datas Acolhimento", "ATENDIMENTOS_AGENDA_Datas Prescrição", "last_stage_concluded",
                     "process_time"
                       ], inplace=True)


data = pd.get_dummies(data,columns=["FUNIL_ASSINATURA_PIPEDRIVE_status"], prefix='assinatura_status')
data = pd.get_dummies(data,columns=['FUNIL_ASSINATURA_PIPEDRIVE_lost_reason'], prefix='assinatura_lost_reason')

st.markdown("### Método Elbow para Determinar o Número de Clusters")

for indice, linha in data['assinatura_status_lost'].items():
  if linha != 1:
    data.drop(indice, inplace=True)

# Drop ObjectId column
data = data.drop(columns=['_id'])

scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Generate concave increasing data
X, y = dg.concave_increasing()

# Find the knee
kl = KneeLocator(X, y, curve="concave")

# Create a plot
fig, ax = plt.subplots()
ax.plot(X, y, label="Data")
ax.scatter([kl.knee], [kl.knee_y], color="red", label="Knee Point", zorder=5)
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_title("Knee Plot")
ax.legend()
ax.grid(True)

# Display the plot in Streamlit
st.pyplot(fig)

st.markdown("### Distribuição do Tempo de Permanência por Cluster (conjunto de treinamento)")
X = data.drop(columns=['stay_time'])  
y = data['stay_time']  


# Your existing code with slight modifications for Streamlit
X = data.drop(columns=['stay_time'])  
y = data['stay_time']  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
kmeans = KMeans(n_clusters=2, random_state=42)
X_train['cluster'] = kmeans.fit_predict(X_train)
X_test['cluster'] = kmeans.predict(X_test)

silhouette_train = silhouette_score(X_train, X_train['cluster'])
silhouette_test = silhouette_score(X_test, X_test['cluster'])
    
ari_train = adjusted_rand_score(y_train, X_train['cluster'])
ari_test = adjusted_rand_score(y_test, X_test['cluster'])

# Plotting for Streamlit
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='cluster', y='stay_time', data=X_train.join(data['stay_time']), ax=ax, palette="Set2")
ax.set_title('Distribuição do Tempo de Permanência por Cluster (conjunto de treinamento)')
ax.set_xlabel('Cluster')
ax.set_ylabel('Tempo de Permanência')
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='cluster', y='stay_time', data=X_test.join(data['stay_time']), ax=ax, palette="Set3")
ax.set_title('Distribuição do Tempo de Permanência por Cluster (conjunto de teste)')
ax.set_xlabel('Cluster')
ax.set_ylabel('Tempo de Permanência')
st.pyplot(fig)

st.markdown("### PCA scatterplot")


kmeans = KMeans(n_clusters=2, random_state=42)
X_train['cluster'] = kmeans.fit_predict(X_train.drop(columns=['cluster']))
X_test['cluster'] = kmeans.predict(X_test.drop(columns=['cluster']))

pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train.drop(columns=['cluster']))
X_test_pca = pca.transform(X_test.drop(columns=['cluster']))

explained_variance_ratio = pca.explained_variance_ratio_


pca_df_train = pd.DataFrame(X_train_pca, columns=['pc1', 'pc2'])
pca_df_train['cluster'] = X_train['cluster']
pca_df_train['target'] = y_train

pca_df_test = pd.DataFrame(X_test_pca, columns=['pc1', 'pc2'])
pca_df_test['cluster'] = X_test['cluster']
pca_df_test['target'] = y_test

cluster_labels = {0: 'Cluster 0', 1: 'Cluster 1'}
pca_df_train['cluster'] = pca_df_train['cluster'].map(cluster_labels)
pca_df_test['cluster'] = pca_df_test['cluster'].map(cluster_labels)

# Plot para o conjunto de treinamento
fig, ax = plt.subplots(figsize=(18, 14))
sns.scatterplot(x='pc1', y='pc2', hue='cluster', data=pca_df_train, palette='Set1', s=100, ax=ax)
ax.set_title('PCA aplicado nos resultados do cluster (Conjunto de Treinamento)')
ax.set_xlabel('Componente principal 1')
ax.set_ylabel('Componente principal 2')
st.pyplot(fig)

# Plot para o conjunto de teste
fig, ax = plt.subplots(figsize=(18, 14))
sns.scatterplot(x='pc1', y='pc2', hue='cluster', data=pca_df_test, palette='Set1', s=100, ax=ax)
ax.set_title('PCA aplicado nos resultados do cluster (Conjunto de Teste)')
ax.set_xlabel('Componente principal 1')
ax.set_ylabel('Componente principal 2')
st.pyplot(fig)