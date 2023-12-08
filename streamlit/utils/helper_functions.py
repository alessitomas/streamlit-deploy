import pandas as pd
from pymongo import MongoClient
from data_preprocessing import preprocessing
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

#--------------------------------- Gráficos ---------------------------------#

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



def plot_graphic_2(df):
    # Convertendo as colunas de data para datetime
    df['PESSOA_PIPEDRIVE_contract_start_date'] = pd.to_datetime(df['PESSOA_PIPEDRIVE_contract_start_date'])
    df['PESSOA_PIPEDRIVE_contract_end_date'] = pd.to_datetime(df['PESSOA_PIPEDRIVE_contract_end_date'])

    # Determinando a data atual para identificar churns
    current_date = datetime.now()

    # Identificando churns (datas de término de contrato no passado)
    df['is_churn'] = df['PESSOA_PIPEDRIVE_contract_end_date'] < current_date

    # Agrupando por mês e ano para análise de tendência de churn
    df['End_Month_Year'] = df['PESSOA_PIPEDRIVE_contract_end_date'].dt.to_period('M')
    churn_counts = df[df['is_churn']]['End_Month_Year'].value_counts().sort_index()

    # Criando o gráfico de previsão de churn e mudar a cor da linha
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=churn_counts.index.astype(str),
        y=churn_counts,
        name='Churn',
        line=dict(color='orchid', width=4)
    ))

    fig.update_layout(
        title='Tendências de Churn por Mês',
        xaxis_title='Ano e Mês',
        yaxis_title='Quantidade de Churns',
        barmode='group'
    )
    st.plotly_chart(fig)


def plot_graphic_3(df):

    # Contagem dos motivos de encerramento de contrato de assinatura
    lost_reason_assinatura = df['FUNIL_ASSINATURA_PIPEDRIVE_lost_reason'].value_counts()

    # Criando o gráfico de pizza
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=lost_reason_assinatura.index,
        values=lost_reason_assinatura,
        name='Motivos de Encerramento de Contrato de Assinatura'
    ))

    fig.update_layout(
        title='Distribuição dos Motivos de Encerramento de Contrato de Assinatura (Gráfico de Pizza)'
    )

    st.plotly_chart(fig)

def plot_graphic_4(df):

    # Convertendo as datas para o formato datetime
    df['PESSOA_PIPEDRIVE_contract_end_date'] = pd.to_datetime(df['PESSOA_PIPEDRIVE_contract_end_date'])

    # Determinando a data atual para identificar churns
    current_date = datetime.now()

    # Identificando churns (datas de término de contrato no passado)
    df['is_churn'] = df['PESSOA_PIPEDRIVE_contract_end_date'] < current_date

    # Filtrando apenas os registros onde houve encerramento de contrato (churn)
    churned_df = df[df['is_churn']]

    # Contagem da distribuição de idade
    age_distribution = churned_df['PESSOA_PIPEDRIVE_age'].value_counts()
    age_distribution = age_distribution[age_distribution.index.notnull()]
    age_distribution = age_distribution[age_distribution.index > 0]

    # Criando o gráfico de distribuição de idade
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=age_distribution.index,
        y=age_distribution,
        name='Idade das Pessoas que Encerraram Contrato'
    ))

    fig.update_layout(
        title='Distribuição de Idade das Pessoas que Encerraram Contrato',
        xaxis_title='Idade',
        yaxis_title='Quantidade',
        xaxis={'categoryorder':'total descending'}
    )

    st.plotly_chart(fig)

def plot_graphic_5(df):

    # Convertendo as datas para o formato datetime
    df['PESSOA_PIPEDRIVE_contract_end_date'] = pd.to_datetime(df['PESSOA_PIPEDRIVE_contract_end_date'])

    # Determinando a data atual para identificar churns
    current_date = datetime.now()

    # Identificando churns (datas de término de contrato no passado)
    df['is_churn'] = df['PESSOA_PIPEDRIVE_contract_end_date'] < current_date

    # Filtrando apenas os registros onde houve encerramento de contrato (churn)
    churned_df = df[df['is_churn']]

    # Contagem da distribuição de cidades que os clientes sao
    city_distribution = churned_df['PESSOA_PIPEDRIVE_city'].value_counts()
    city_distribution = city_distribution[city_distribution.index.notnull()]
    # se tiver menos que 10 clientes na cidade, colocar em uma categoria outros
    city_distribution['Outros'] = city_distribution[city_distribution < 5].sum()
    city_distribution = city_distribution[city_distribution >= 5]

    # Criando o gráfico de distribuição de tempo que as pessoas ficaram na plataforma
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=city_distribution.index,
        values=city_distribution,
        name='Cidades em que os clientes vivem'
    ))

    fig.update_layout(
        title='Cidades em que os clientes vivem',
        xaxis_title='Cidades',
        yaxis_title='Quantidade',
        xaxis={'categoryorder':'total descending'}
    )

    st.plotly_chart(fig)

def plot_graphic_6(df):

    # Convertendo as datas para o formato datetime
    df['PESSOA_PIPEDRIVE_contract_end_date'] = pd.to_datetime(df['PESSOA_PIPEDRIVE_contract_end_date'])

    # Determinando a data atual para identificar churns
    current_date = datetime.now()

    # Identificando churns (datas de término de contrato no passado)
    df['is_churn'] = df['PESSOA_PIPEDRIVE_contract_end_date'] < current_date

    # Filtrando apenas os registros onde houve encerramento de contrato (churn)
    churned_df = df[df['is_churn']]

    # Contagem da distribuição de pessoa tem canal de contato de preferencia

    contact_distribution = churned_df["PESSOA_PIPEDRIVE_Tem_Canal_de_Preferência"].value_counts()
    contact_distribution = contact_distribution[contact_distribution.index.notnull()]

    # se for 1, é sim, se for 0, é não
    contact_distribution.index = ['Sim', 'Não']

    # Criando o gráfico de distribuição de tempo que as pessoas ficaram na plataforma
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=contact_distribution.index,
        values=contact_distribution,
        name='Tem Canal de Preferência'
    ))

    fig.update_layout(
        title='Tem Canal de Preferência',
        xaxis_title='Canal de Preferência',
        yaxis_title='Quantidade',
        xaxis={'categoryorder':'total descending'}
    )

    st.plotly_chart(fig)
    
def plot_graphic_7(df):

    # Convertendo as datas para o formato datetime
    df['PESSOA_PIPEDRIVE_contract_end_date'] = pd.to_datetime(df['PESSOA_PIPEDRIVE_contract_end_date'])

    # Determinando a data atual para identificar churns
    current_date = datetime.now()

    # Identificando churns (datas de término de contrato no passado)
    df['is_churn'] = df['PESSOA_PIPEDRIVE_contract_end_date'] < current_date

    # Filtrando apenas os registros onde houve encerramento de contrato (churn)
    churned_df = df[df['is_churn']]

    # Contagem da distribuição de cidades que os clientes sao
    state_distribution = churned_df['PESSOA_PIPEDRIVE_state'].value_counts()
    state_distribution = state_distribution[state_distribution.index.notnull()]
    # se tiver menos que 10 clientes na cidade, colocar em uma categoria outros
    state_distribution['Outros'] = state_distribution[state_distribution < 7].sum()
    state_distribution = state_distribution[state_distribution >= 7]

    # Criando o gráfico de distribuição de tempo que as pessoas ficaram na plataforma
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=state_distribution.index,
        values=state_distribution,
        name='Estados em que os clientes vivem'
    ))

    fig.update_layout(
        title='Estados em que os clientes vivem',
        xaxis_title='Estados',
        yaxis_title='Quantidade',
        xaxis={'categoryorder':'total descending'}
    )

    st.plotly_chart(fig)

def plot_graphic_8(df):

    # Convertendo as datas para o formato datetime
    df['PESSOA_PIPEDRIVE_contract_end_date'] = pd.to_datetime(df['PESSOA_PIPEDRIVE_contract_end_date'])

    # Determinando a data atual para identificar churns
    current_date = datetime.now()

    # Identificando churns (datas de término de contrato no passado)
    df['is_churn'] = df['PESSOA_PIPEDRIVE_contract_end_date'] < current_date

    # Filtrando apenas os registros onde houve encerramento de contrato (churn)
    churned_df = df[df['is_churn']]

    # Contagem da distribuição de genero

    gender_distribution = churned_df['PESSOA_PIPEDRIVE_id_gender'].value_counts()
    gender_distribution = gender_distribution[gender_distribution.index.notnull()]


    # se for 64 é masculino, se for 63 é feminino

    gender_distribution.index = ['Masculino', 'Feminino', 'Outros', 'Não informado']

    # Criando o gráfico de distribuição de tempo que as pessoas ficaram na plataforma

    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=gender_distribution.index,
        values=gender_distribution,
        name='Gênero dos clientes'
    ))

    fig.update_layout(
        title='Gênero dos clientes',
        xaxis_title='Gênero',
        yaxis_title='Quantidade',
        xaxis={'categoryorder':'total descending'}
    )

    st.plotly_chart(fig)

def plot_graphic_9(df):

    # Convertendo as datas para o formato datetime
    df['PESSOA_PIPEDRIVE_contract_end_date'] = pd.to_datetime(df['PESSOA_PIPEDRIVE_contract_end_date'])

    # Determinando a data atual para identificar churns
    current_date = datetime.now()

    # Identificando churns (datas de término de contrato no passado)
    df['is_churn'] = df['PESSOA_PIPEDRIVE_contract_end_date'] < current_date

    # Filtrando apenas os registros onde houve encerramento de contrato (churn)
    churned_df = df[df['is_churn']]

    # Contagem da distribuição de tipos de preferencia de contato

    contact_type_distribution = churned_df["PESSOA_PIPEDRIVE_Canal de Preferência"].value_counts()
    contact_type_distribution = contact_type_distribution[contact_type_distribution.index.notnull()]

    # se for 0 é mensagem, se for 1 é ligação

    contact_type_distribution.index = ['Mensagem', 'Ligação', 'Outros', 'Não informado']

    # Criando o gráfico de distribuição de tempo que as pessoas ficaram na plataforma

    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=contact_type_distribution.index,
        values=contact_type_distribution,
        name='Tipo de contato preferido'
    ))

    fig.update_layout(
        title='Tipo de contato preferido',
        xaxis_title='Tipo de contato',
        yaxis_title='Quantidade',
        xaxis={'categoryorder':'total descending'}
    )

    st.plotly_chart(fig)

def plot_graphic_10(df):

    df['PESSOA_PIPEDRIVE_contract_start_date'] = pd.to_datetime(df['PESSOA_PIPEDRIVE_contract_start_date'])
    df['PESSOA_PIPEDRIVE_contract_end_date'] = pd.to_datetime(df['PESSOA_PIPEDRIVE_contract_end_date'])
    df['Start_Year'] = df['PESSOA_PIPEDRIVE_contract_start_date'].dt.to_period('Y')
    df['End_Year'] = df['PESSOA_PIPEDRIVE_contract_end_date'].dt.to_period('Y')
    start_counts = df['Start_Year'].value_counts().sort_index()
    end_counts = df['End_Year'].value_counts().sort_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=start_counts.index.astype(str), y=start_counts, name='Entradas'))
    fig.add_trace(go.Bar(x=end_counts.index.astype(str), y=end_counts, name='Saídas'))
    fig.update_layout(
        title='Histograma de Entrada e Saída de Assinaturas por Ano',
        xaxis_title='Ano',
        yaxis_title='Quantidade de Assinaturas',
        barmode='group'
    )
    st.plotly_chart(fig)

#-----------------------------------------------------------------------------#

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