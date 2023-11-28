import pandas as pd
from pymongo import MongoClient
from data_preprocessing import preprocessing
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
import bcrypt

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

def create_user(url, db_name, collection_name, username, password):
    client = MongoClient(url)  
    db = client[db_name]
    collection = db[collection_name]

    if collection.find_one({"username": username}):
        return False, "Usuário já existe"

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user_data = {
        "username": username,
        "password": hashed_password
    }

    collection.insert_one(user_data)

    return True, "Usuário criado com sucesso"

def verify_credentials(url, db_name, collection_name, username, password):
    client = MongoClient(url)  
    db = client[db_name]
    collection = db[collection_name]
    user = collection.find_one({"username": username})

    if not user:
        return False, f"Usuário: {username} não existe"
    
    if bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return True, "Login bem-sucedido"
    else:
        return False, "Senha incorreta"


def check_authentication():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("Você precisa estar logado para acessar esta página.")
        st.stop()


def logged_out_option():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        with st.sidebar:
            if st.button('Logout'):
                # Perform logout actions here
                st.session_state.logged_in = False
                st.rerun()  # This will refresh the page, effectively logging the user out