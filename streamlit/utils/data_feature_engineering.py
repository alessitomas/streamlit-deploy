import pandas as pd
import numpy as np
from category_encoders import CountEncoder
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from scipy import stats
from datetime import datetime
from sklearn.utils import resample


def feature_engineering(dataframe):

    # feature engineering 1 + 3


    dataframe["ATENDIMENTOS_AGENDA_Qde Atendimentos Acolhimento"].fillna(0,inplace=True)
    dataframe["ATENDIMENTOS_AGENDA_Faltas Acolhimento"].fillna(0,inplace=True)
    dataframe["ATENDIMENTOS_AGENDA_Datas Acolhimento"].fillna("Nunca ocorreu",inplace=True)
    dataframe = dataframe[~dataframe['ATENDIMENTOS_AGENDA_Datas Acolhimento'].astype(str).str.contains("Nunca ocorreu")]

    dataframe = dataframe.explode('ATENDIMENTOS_AGENDA_Datas Acolhimento')
    dataframe["TWILIO_Mensagens Já Enviou"] = dataframe["TWILIO_Mensagens Inbound"] > 0
    dataframe["TWILIO_Mensagens Razão"] = dataframe["TWILIO_Mensagens Outbound"] / dataframe["TWILIO_Mensagens Inbound"].where(dataframe["TWILIO_Mensagens Já Enviou"], 1)
    
    dataframe["PESSOA_PIPEDRIVE CRIANÇA"] = dataframe["PESSOA_PIPEDRIVE_age"] <= 16
    dataframe["PESSOA_PIPEDRIVE CRIANÇA"].fillna(0)
    dataframe["PESSOA_PIPEDRIVE CRIANÇA"].replace(True, 1, inplace=True)
    dataframe["PESSOA_PIPEDRIVE CRIANÇA"].replace(False, 0, inplace=True)
    
    dataframe["PESSOA_PIPEDRIVE JOVEM"] = (dataframe["PESSOA_PIPEDRIVE_age"] > 16) & (dataframe["PESSOA_PIPEDRIVE_age"] <= 30)
    dataframe["PESSOA_PIPEDRIVE JOVEM"].fillna(0)
    dataframe["PESSOA_PIPEDRIVE JOVEM"].replace(True, 1, inplace=True)
    dataframe["PESSOA_PIPEDRIVE JOVEM"].replace(False, 0, inplace=True)

    dataframe["PESSOA_PIPEDRIVE ADULTO"] = (dataframe["PESSOA_PIPEDRIVE_age"] > 30) & (dataframe["PESSOA_PIPEDRIVE_age"] <= 60)
    dataframe["PESSOA_PIPEDRIVE ADULTO"].fillna(0)
    dataframe["PESSOA_PIPEDRIVE ADULTO"].replace(True, 1, inplace=True)
    dataframe["PESSOA_PIPEDRIVE ADULTO"].replace(False, 0, inplace=True)

    dataframe["PESSOA_PIPEDRIVE IDOSO"] = dataframe["PESSOA_PIPEDRIVE_age"] > 60
    dataframe["PESSOA_PIPEDRIVE IDOSO"].fillna(0)
    dataframe["PESSOA_PIPEDRIVE IDOSO"].replace(True, 1, inplace=True)
    dataframe["PESSOA_PIPEDRIVE IDOSO"].replace(False, 0, inplace=True)


    dataframe["TWILIO_Ligações Outbound Qtd Significativa"] = dataframe["TWILIO_Ligações Outbound"] >= dataframe["TWILIO_Ligações Outbound"].mean()
    dataframe["TWILIO_Ligações Outbound Qtd Significativa"].fillna(0)
    dataframe["TWILIO_Ligações Outbound Qtd Significativa"].replace(True, 1, inplace=True)
    dataframe["TWILIO_Ligações Outbound Qtd Significativa"].replace(False, 0, inplace=True)
    
    dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia Nenhum"] = dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia"] == 0
    dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia Nenhum"].fillna(0)
    dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia Nenhum"].replace(True, 1, inplace=True)
    dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia Nenhum"].replace(False, 0, inplace=True)

    dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia Pouco"] = (dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia"] > 0) & (dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia"] <= dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia"].mean() )
    dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia Pouco"].fillna(0)
    dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia Pouco"].replace(True, 1, inplace=True)
    dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia Pouco"].replace(False, 0, inplace=True)
    
    dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia Muito"] = dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia"] > dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia"].mean() 
    dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia Muito"].fillna(0)
    dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia Muito"].replace(True, 1, inplace=True)
    dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia Muito"].replace(False, 0, inplace=True)
    
    dataframe["ATENDIMENTOS_AGENDA_Qde Prescrições"].fillna(0,inplace=True)

    dataframe = dataframe.drop(["ATENDIMENTOS_AGENDA_Datas Prescrição"],axis=1)

    dataframe = dataframe[dataframe["PESSOA_PIPEDRIVE_id_gender"].isin([64,63])]   
    dataframe["PESSOA_PIPEDRIVE_id_gender Binário"] = dataframe["PESSOA_PIPEDRIVE_id_gender"].map({64: 0, 63: 1})

    dataframe = dataframe[dataframe["FUNIL_ASSINATURA_PIPEDRIVE_id_stage"].isin([65,64])]   
    dataframe["FUNIL_ASSINATURA_PIPEDRIVE_id_stage Binário"] = dataframe["FUNIL_ASSINATURA_PIPEDRIVE_id_stage"].map({65: 0, 64: 1})



    dataframe = pd.get_dummies(dataframe, columns=['PESSOA_PIPEDRIVE_id_marrital_status'], prefix='Status')
    dataframe = pd.get_dummies(dataframe, columns=['PESSOA_PIPEDRIVE_state'], prefix='Estado')

    ce = CountEncoder()
    dataframe['PESSOA_PIPEDRIVE_city Codificada'] = ce.fit_transform(dataframe['PESSOA_PIPEDRIVE_city'])

    
    dataframe = dataframe.drop(columns=["PESSOA_PIPEDRIVE_postal_code","PESSOA_PIPEDRIVE_id_person","PESSOA_PIPEDRIVE_city","PESSOA_PIPEDRIVE_id_gender","FUNIL_ASSINATURA_PIPEDRIVE_id_stage","FUNIL_ASSINATURA_PIPEDRIVE_id_org","FUNIL_ONBOARDING_PIPEDRIVE_add_time","ATENDIMENTOS_AGENDA_Datas Atendimento Médico","ATENDIMENTOS_AGENDA_Datas Acolhimento","process_time"])

    # feature engineering 2 + 1

    dataframe = pd.get_dummies(dataframe,columns=["FUNIL_ASSINATURA_PIPEDRIVE_status"], prefix='assinatura_status')
    dataframe = pd.get_dummies(dataframe,columns=['FUNIL_ASSINATURA_PIPEDRIVE_lost_reason'], prefix='assinatura_lost_reason')
    dataframe = pd.get_dummies(dataframe,columns=['PESSOA_PIPEDRIVE_Canal de Preferência'], prefix='canal_preferencia')    
    dataframe = pd.get_dummies(dataframe,columns=['FUNIL_ONBOARDING_PIPEDRIVE_status'], prefix='onboarding_status')
    dataframe = pd.get_dummies(dataframe,columns=['FUNIL_ONBOARDING_PIPEDRIVE_lost_reason'], prefix='onboarding_lost_reason')

    tempo_permanencia = []

    for indice, valor in dataframe["FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"].items():
        if pd.notna(valor):
            index = dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"].find(";")
            if index != -1:
                dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"] = dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"][:index]

    for indice, valor in dataframe["FUNIL_ASSINATURA_PIPEDRIVE_lost_time"].items():
        if pd.notna(dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"]):
            tempo_1 = datetime.strptime(dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"], '%Y-%m-%d')
            tempo_2 = datetime.strptime(dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"], '%Y-%m-%d')
            tempo_permanencia.append(str(tempo_1 - tempo_2))
        else:
            tempo_1 = datetime.strptime(dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"], '%Y-%m-%d')
            tempo_2 = datetime.strptime(dataframe.loc[indice, "PESSOA_PIPEDRIVE_contract_start_date"], '%Y-%m-%d')
            tempo_permanencia.append(str(tempo_1 - tempo_2))

    dataframe['stay_time'] = tempo_permanencia

    for indice, valor in dataframe["stay_time"].items():
        index = dataframe.loc[indice, "stay_time"].find(",")
        if index != -1:
            dataframe.loc[indice, "stay_time"] = dataframe.loc[indice, "stay_time"][:index]

    dataframe["stay_time"] = dataframe["stay_time"].str.extract('(\d+) days').astype(float)
    dataframe["stay_time"] = np.nan_to_num(dataframe["stay_time"], nan=0)

    dataframe.drop(columns=["FUNIL_ASSINATURA_PIPEDRIVE_start_of_service","FUNIL_ASSINATURA_PIPEDRIVE_lost_time","PESSOA_PIPEDRIVE_contract_start_date","PESSOA_PIPEDRIVE_contract_end_date"],inplace=True)

    # feature engineering 4 

    if dataframe['WHOQOL_Físico_New'].dtype == 'object':
        # Aplicando codificação one-hot para variáveis categóricas
        encoder = OneHotEncoder()
        encoded = encoder.fit_transform(dataframe[['WHOQOL_Físico_New']])
        encoded_df = pd.DataFrame(encoded.toarray(), columns=encoder.get_feature_names_out(['WHOQOL_Físico_New']))
        dataframe = dataframe.join(encoded_df)
    else:
        # Aplicando normalização ou padronização para variáveis numéricas
        scaler = StandardScaler()
        dataframe['WHOQOL_Físico_New'] = scaler.fit_transform(dataframe[['WHOQOL_Físico_New']])

    # Calculando o intervalo interquartil
    Q1 = dataframe['WHOQOL_Físico_New'].quantile(0.25)
    Q3 = dataframe['WHOQOL_Físico_New'].quantile(0.75)
    IQR = Q3 - Q1

    # Removendo os outliers
    dataframe = dataframe[(dataframe['WHOQOL_Físico_New'] >= Q1 - 1.5 * IQR) & (dataframe['WHOQOL_Físico_New'] <= Q3 + 1.5 * IQR)]

    # Verificando se é categórica ou numérica
    if dataframe['WHOQOL_Psicológico_New'].dtype == 'object':
        # Aplicando codificação one-hot para variáveis categóricas
        encoder = OneHotEncoder()
        encoded = encoder.fit_transform(dataframe[['WHOQOL_Psicológico_New']])
        encoded_df = pd.DataFrame(encoded.toarray(), columns=encoder.get_feature_names_out(['WHOQOL_Psicológico_New']))
        dataframe = dataframe.join(encoded_df)
    else:
        # Aplicando normalização ou padronização para variáveis numéricas
        scaler = StandardScaler()
        dataframe['WHOQOL_Psicológico_New'] = scaler.fit_transform(dataframe[['WHOQOL_Psicológico_New']])

        # Calculando o intervalo interquartil
        Q1 = dataframe['WHOQOL_Psicológico_New'].quantile(0.25)
        Q3 = dataframe['WHOQOL_Psicológico_New'].quantile(0.75)
        IQR = Q3 - Q1

        # Removendo os outliers
        dataframe = dataframe[(dataframe['WHOQOL_Psicológico_New'] >= Q1 - 1 * IQR) & (dataframe['WHOQOL_Psicológico_New'] <= Q3 + 1 * IQR)]

    # Verificando se é categórica ou numérica
    if dataframe['WHOQOL_Social_New'].dtype == 'object':
        # Aplicando codificação one-hot para variáveis categóricas
        encoder = OneHotEncoder()
        encoded = encoder.fit_transform(dataframe[['WHOQOL_Social_New']])
        encoded_df = pd.DataFrame(encoded.toarray(), columns=encoder.get_feature_names_out(['WHOQOL_Social_New']))
        data = data.join(encoded_df)
    else:
        # Aplicando normalização ou padronização para variáveis numéricas
        scaler = StandardScaler()
        dataframe['WHOQOL_Social_New'] = scaler.fit_transform(dataframe[['WHOQOL_Social_New']])

    Q1 = dataframe['WHOQOL_Social_New'].quantile(0.25)
    Q3 = dataframe['WHOQOL_Social_New'].quantile(0.75)
    IQR = Q3 - Q1

    # Removendo os outliers
    dataframe = dataframe[(dataframe['WHOQOL_Social_New'] >= Q1 - 1 * IQR) & (dataframe['WHOQOL_Social_New'] <= Q3 + 1 * IQR)]

    dataframe = pd.get_dummies(dataframe, columns=['last_stage_concluded'], prefix='stage')

    dataframe.to_csv('../notebooks/data/data-engineering.csv', index=False)

    return dataframe


    


