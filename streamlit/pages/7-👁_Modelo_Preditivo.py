import pandas as pd
from datetime import datetime 
import numpy as np
from sklearn.discriminant_analysis import StandardScaler
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

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

for indice, linha in data['assinatura_status_lost'].items():
  if linha != 1:
    data.drop(indice, inplace=True)

# Drop ObjectId column
data = data.drop(columns=['_id'])

scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

inertia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data_scaled)
    inertia.append(kmeans.inertia_)

# Elbow method plot
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), inertia, marker='o', color='blue')
plt.title('Método Elbow para Determinar o Número de Clusters', fontsize=16)
plt.xlabel('Número de Clusters', fontsize=14)
plt.ylabel('Inércia', fontsize=14)
st.pyplot(plt.gcf())  # Display the plot in Streamlit
plt.clf()  # Clear the current figure

X = data.drop(columns=['stay_time'])  
y = data['stay_time']  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

kmeans = KMeans(n_clusters=8, random_state=42)
X_train['cluster'] = kmeans.fit_predict(X_train)

X_test['cluster'] = kmeans.predict(X_test)

silhouette_train = silhouette_score(X_train, X_train['cluster'])
silhouette_test = silhouette_score(X_test, X_test['cluster'])

print(f"Silhouette Score (Training): {silhouette_train}")
print(f"Silhouette Score (Testing): {silhouette_test}")

ari_train = adjusted_rand_score(y_train, X_train['cluster'])
ari_test = adjusted_rand_score(y_test, X_test['cluster'])

print(f"Adjusted Rand Index (Training): {ari_train}")
print(f"Adjusted Rand Index (Testing): {ari_test}")

# Boxplot for training data
plt.figure(figsize=(10, 6))
sns.boxplot(x='cluster', y=data['stay_time'], data=X_train, palette='viridis')
plt.title('Distribuição do Tempo de Permanência por Cluster (conjunto de treinamento)', fontsize=16)
plt.xlabel('Cluster', fontsize=14)
plt.ylabel('Tempo de Permanência', fontsize=14)
st.pyplot(plt.gcf())  # Display the plot in Streamlit
plt.clf()  # Clear the current figure

# Boxplot for testing data
plt.figure(figsize=(10, 6))
sns.boxplot(x='cluster', y=data['stay_time'], data=X_test, palette='viridis')
plt.title('Distribuição do Tempo de Permanência por Cluster (conjunto de teste)', fontsize=16)
plt.xlabel('Cluster', fontsize=14)
plt.ylabel('Tempo de Permanência', fontsize=14)
st.pyplot(plt.gcf())  # Display the plot in Streamlit
plt.clf()  # Clear the current figure

X = data.drop(columns=['stay_time'])
y = data['stay_time']

pca = PCA(n_components=2) 
X_pca = pca.fit_transform(X)

pca_df = pd.DataFrame(X_pca, columns=['pc1', 'pc2'])
pca_df['target'] = y

# PCA scatterplot
plt.figure(figsize=(18, 14))
sns.scatterplot(x='pc1', y='pc2', hue='target', data=pca_df, palette='coolwarm')
plt.title('PCA aplicado no dataset', fontsize=20)
plt.xlabel('Componente principal 1', fontsize=18)
plt.ylabel('Componente principal 2', fontsize=18)
st.pyplot(plt.gcf())  # Display the plot in Streamlit

