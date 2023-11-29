import pandas as pd
from pymongo import MongoClient
from data_preprocessing import preprocessing
import pandas as pd
from datetime import datetime
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
    st.plotly_chart(fig)

def create_user(url, db_name, collection_name, username, password, role):
    client = MongoClient(url)  
    db = client[db_name]
    collection = db[collection_name]
    if collection.find_one({"username": username}):
        return False, "Usuário já existe"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_data = {
        "username": username,
        "password": hashed_password,
        "role": [role]
    }
    collection.insert_one(user_data)
    return True, "Usuário criado com sucesso"

def verify_credentials(url, db_name, collection_name, username, password):
    client = MongoClient(url)  
    db = client[db_name]
    collection = db[collection_name]
    user = collection.find_one({"username": username})
    if not user:
        return False, f"Usuário: {username} não existe", None
    if bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return True, "Login bem-sucedido", user['role'][0]
    else:
        return False, "Senha incorreta", None


def check_authentication():
    if 'logged_in' not in st.session_state or st.session_state.logged_in == None:
        st.error("Você precisa estar logado para acessar esta página.")
        st.stop()


def logged_out_option():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        with st.sidebar:
            if st.button('Logout'):
                st.session_state.logged_in = None
                st.session_state.Admin = False
                st.rerun()  


def get_logs(url, db_name, collection_name):
    client = MongoClient(url)
    db = client[db_name]
    collection = db[collection_name]
    logs_cursor = collection.find({}, {"_id": 0, "user": 1, "action": 1, "timestamp": 1})
    logs = list(logs_cursor)
    if len(logs) == 0:

        return []
    else:
        logs_details = [(log["user"], log["action"], log["timestamp"]) for log in logs]
        return logs_details
    
def add_log(url, db_name, collection_name, user, action):
    current_timestamp = datetime.now()
    formatted_timestamp = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    client = MongoClient(url)  
    db = client[db_name]
    collection = db[collection_name]
    log = {
        "user": user,
        "action": action,
        "timestamp": formatted_timestamp
    }
    collection.insert_one(log)