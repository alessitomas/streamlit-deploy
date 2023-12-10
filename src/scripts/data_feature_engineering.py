import pandas as pd
import numpy as np
from category_encoders import CountEncoder
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from datetime import datetime

def feature_engineering(data_pre):

    # feature engineering 1 + 3

    data_pre["ATENDIMENTOS_AGENDA_Qde Atendimentos Acolhimento"].fillna(0,inplace=True)
    data_pre["ATENDIMENTOS_AGENDA_Faltas Acolhimento"].fillna(0,inplace=True)
    data_pre["ATENDIMENTOS_AGENDA_Datas Acolhimento"].fillna("Nunca ocorreu",inplace=True)

    data_pre = data_pre[~data_pre['ATENDIMENTOS_AGENDA_Datas Acolhimento'].astype(str).str.contains("Nunca ocorreu")]

    data_pre = data_pre.explode('ATENDIMENTOS_AGENDA_Datas Acolhimento')

    data_pre["TWILIO_Mensagens Já Enviou"] = int(data_pre["TWILIO_Mensagens Inbound"].iloc[0]) > 0
    data_pre["TWILIO_Mensagens Razão"] = int(data_pre["TWILIO_Mensagens Outbound"].iloc[0]) / int(data_pre["TWILIO_Mensagens Inbound"].where(data_pre["TWILIO_Mensagens Já Enviou"], 1).iloc[0])

    data_pre["PESSOA_PIPEDRIVE CRIANÇA"] = data_pre["PESSOA_PIPEDRIVE_age"] <= 16
    data_pre["PESSOA_PIPEDRIVE CRIANÇA"].fillna(0)
    data_pre["PESSOA_PIPEDRIVE CRIANÇA"].replace(True, 1, inplace=True)
    data_pre["PESSOA_PIPEDRIVE CRIANÇA"].replace(False, 0, inplace=True)

    data_pre["PESSOA_PIPEDRIVE JOVEM"] = (data_pre["PESSOA_PIPEDRIVE_age"] > 16) & (data_pre["PESSOA_PIPEDRIVE_age"] <= 30)
    data_pre["PESSOA_PIPEDRIVE JOVEM"].fillna(0)
    data_pre["PESSOA_PIPEDRIVE JOVEM"].replace(True, 1, inplace=True)
    data_pre["PESSOA_PIPEDRIVE JOVEM"].replace(False, 0, inplace=True)

    data_pre["PESSOA_PIPEDRIVE ADULTO"] = (data_pre["PESSOA_PIPEDRIVE_age"] > 30) & (data_pre["PESSOA_PIPEDRIVE_age"] <= 60)
    data_pre["PESSOA_PIPEDRIVE ADULTO"].fillna(0)
    data_pre["PESSOA_PIPEDRIVE ADULTO"].replace(True, 1, inplace=True)
    data_pre["PESSOA_PIPEDRIVE ADULTO"].replace(False, 0, inplace=True)

    data_pre["PESSOA_PIPEDRIVE IDOSO"] = data_pre["PESSOA_PIPEDRIVE_age"] > 60
    data_pre["PESSOA_PIPEDRIVE IDOSO"].fillna(0)
    data_pre["PESSOA_PIPEDRIVE IDOSO"].replace(True, 1, inplace=True)
    data_pre["PESSOA_PIPEDRIVE IDOSO"].replace(False, 0, inplace=True)


    data_pre["ATENDIMENTOS_AGENDA_Qde Prescrições"].fillna(0,inplace=True)

    data_pre = data_pre.drop(["ATENDIMENTOS_AGENDA_Datas Prescrição"],axis=1)


    data_pre = data_pre[data_pre["PESSOA_PIPEDRIVE_id_gender"].isin(['64','63'])]   
    data_pre["PESSOA_PIPEDRIVE_id_gender Binário"] = data_pre["PESSOA_PIPEDRIVE_id_gender"].map({'64': 0, '63': 1})

    data_pre = data_pre[data_pre["FUNIL_ASSINATURA_PIPEDRIVE_id_stage"].isin(['65','64'])]   
    data_pre["FUNIL_ASSINATURA_PIPEDRIVE_id_stage Binário"] = data_pre["FUNIL_ASSINATURA_PIPEDRIVE_id_stage"].map({'65': 0, '64': 1})

    data_pre = pd.get_dummies(data_pre, columns=['PESSOA_PIPEDRIVE_id_marrital_status'], prefix='Status')
    data_pre = pd.get_dummies(data_pre, columns=['PESSOA_PIPEDRIVE_state'], prefix='Estado')

    ce = CountEncoder()
    data_pre['PESSOA_PIPEDRIVE_city Codificada'] = ce.fit_transform(data_pre['PESSOA_PIPEDRIVE_city'])

    data_pre = data_pre.drop(columns=["PESSOA_PIPEDRIVE_postal_code","PESSOA_PIPEDRIVE_city","PESSOA_PIPEDRIVE_id_gender","FUNIL_ASSINATURA_PIPEDRIVE_id_stage","FUNIL_ASSINATURA_PIPEDRIVE_id_org","FUNIL_ONBOARDING_PIPEDRIVE_add_time","ATENDIMENTOS_AGENDA_Datas Atendimento Médico","ATENDIMENTOS_AGENDA_Datas Acolhimento","process_time"])

    # feature engineering 2 + 3

    data_pre = pd.get_dummies(data_pre,columns=["FUNIL_ASSINATURA_PIPEDRIVE_status"], prefix='assinatura_status')
    data_pre = pd.get_dummies(data_pre,columns=['FUNIL_ASSINATURA_PIPEDRIVE_lost_reason'], prefix='assinatura_lost_reason')
    data_pre = pd.get_dummies(data_pre,columns=['PESSOA_PIPEDRIVE_Canal de Preferência'], prefix='canal_preferencia')    
    data_pre = pd.get_dummies(data_pre,columns=['FUNIL_ONBOARDING_PIPEDRIVE_status'], prefix='onboarding_status')
    data_pre = pd.get_dummies(data_pre,columns=['FUNIL_ONBOARDING_PIPEDRIVE_lost_reason'], prefix='onboarding_lost_reason')

    tempo_permanencia = []

    for indice, valor in data_pre["FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"].items():
        if pd.notna(valor):
            index = data_pre.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"].find(";")
            if index != -1:
                data_pre.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"] = data_pre.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"][:index]

    for indice, valor in data_pre["FUNIL_ASSINATURA_PIPEDRIVE_lost_time"].items():
        if pd.notna(data_pre.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"]):
            tempo_1 = datetime.strptime(data_pre.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"], '%Y-%m-%d')
            tempo_2 = datetime.strptime(data_pre.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"], '%Y-%m-%d')
            tempo_permanencia.append(str(tempo_1 - tempo_2))
        else:
            tempo_1 = datetime.strptime(data_pre.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"], '%Y-%m-%d')
            tempo_2 = datetime.strptime(data_pre.loc[indice, "PESSOA_PIPEDRIVE_contract_start_date"], '%Y-%m-%d')
            tempo_permanencia.append(str(tempo_1 - tempo_2))
    
    data_pre['stay_time'] = tempo_permanencia

    for indice, valor in data_pre["stay_time"].items():
        index = data_pre.loc[indice, "stay_time"].find(",")
        if index != -1:
            data_pre.loc[indice, "stay_time"] = data_pre.loc[indice, "stay_time"][:index]

    data_pre["stay_time"] = data_pre["stay_time"].str.extract('(\d+) days').astype(float)
    data_pre["stay_time"] = np.nan_to_num(data_pre["stay_time"], nan=0)

    data_pre.drop(columns=["PESSOA_PIPEDRIVE_contract_start_date", "FUNIL_ASSINATURA_PIPEDRIVE_lost_time", "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service", "PESSOA_PIPEDRIVE_contract_end_date"], inplace=True)
   
    # feature engineering 4 + 3

    if data_pre['WHOQOL_Físico_New'].dtype == 'object':
        # Aplicando codificação one-hot para variáveis categóricas
        encoder = OneHotEncoder()
        encoded = encoder.fit_transform(data_pre[['WHOQOL_Físico_New']])
        encoded_df = pd.data_pre(encoded.toarray(), columns=encoder.get_feature_names_out(['WHOQOL_Físico_New']))
        data_pre = data_pre.join(encoded_df)
    else:
        # Aplicando normalização ou padronização para variáveis numéricas
        scaler = StandardScaler()
        if data_pre['WHOQOL_Físico_New'].count() >= 2:
            data_pre['WHOQOL_Físico_New'] = scaler.fit_transform(data_pre[['WHOQOL_Físico_New']])
        else:
            # Lide com o caso de ter apenas uma linha ou todos os valores NaN
            data_pre['WHOQOL_Físico_New'] = data_pre['WHOQOL_Físico_New'].fillna(0)

    # Calculando o intervalo interquartil
    Q1 = data_pre['WHOQOL_Físico_New'].quantile(0.25)
    Q3 = data_pre['WHOQOL_Físico_New'].quantile(0.75)
    IQR = Q3 - Q1

    # Removendo os outliers
    data_pre = data_pre[(data_pre['WHOQOL_Físico_New'] >= Q1 - 1.5 * IQR) & (data_pre['WHOQOL_Físico_New'] <= Q3 + 1.5 * IQR)]



    # Verificando se é categórica ou numérica
    if data_pre['WHOQOL_Psicológico_New'].dtype == 'object':
        # Aplicando codificação one-hot para variáveis categóricas
        encoder = OneHotEncoder()
        encoded = encoder.fit_transform(data_pre[['WHOQOL_Psicológico_New']])
        encoded_df = pd.data_pre(encoded.toarray(), columns=encoder.get_feature_names_out(['WHOQOL_Psicológico_New']))
        data_pre = data_pre.join(encoded_df)
    else:
        # Aplicando normalização ou padronização para variáveis numéricas
        scaler = StandardScaler()
        if data_pre['WHOQOL_Psicológico_New'].count() >= 2:
            data_pre['WHOQOL_Psicológico_New'] = scaler.fit_transform(data_pre[['WHOQOL_Psicológico_New']])
        else:
            # Lide com o caso de ter apenas uma linha ou todos os valores NaN
            data_pre['WHOQOL_Psicológico_New'] = data_pre['WHOQOL_Psicológico_New'].fillna(0)

        # Calculando o intervalo interquartil
        Q1 = data_pre['WHOQOL_Psicológico_New'].quantile(0.25)
        Q3 = data_pre['WHOQOL_Psicológico_New'].quantile(0.75)
        IQR = Q3 - Q1

        # Removendo os outliers
        data_pre = data_pre[(data_pre['WHOQOL_Psicológico_New'] >= Q1 - 1 * IQR) & (data_pre['WHOQOL_Psicológico_New'] <= Q3 + 1 * IQR)]

    # Verificando se é categórica ou numérica
    if data_pre['WHOQOL_Social_New'].dtype == 'object':
        # Aplicando codificação one-hot para variáveis categóricas
        encoder = OneHotEncoder()
        encoded = encoder.fit_transform(data_pre[['WHOQOL_Social_New']])
        encoded_df = pd.data_pre(encoded.toarray(), columns=encoder.get_feature_names_out(['WHOQOL_Social_New']))
        data = data.join(encoded_df)
    else:
        # Aplicando normalização ou padronização para variáveis numéricas
        scaler = StandardScaler()
        if data_pre['WHOQOL_Social_New'].count() >= 2:
            data_pre['WHOQOL_Social_New'] = scaler.fit_transform(data_pre[['WHOQOL_Social_New']])
        else:
            # Lide com o caso de ter apenas uma linha ou todos os valores NaN
            data_pre['WHOQOL_Social_New'] = data_pre['WHOQOL_Social_New'].fillna(0)

    Q1 = data_pre['WHOQOL_Social_New'].quantile(0.25)
    Q3 = data_pre['WHOQOL_Social_New'].quantile(0.75)
    IQR = Q3 - Q1

    # Removendo os outliers
    data_pre = data_pre[(data_pre['WHOQOL_Social_New'] >= Q1 - 1 * IQR) & (data_pre['WHOQOL_Social_New'] <= Q3 + 1 * IQR)]

    data_pre = pd.get_dummies(data_pre, columns=['last_stage_concluded'], prefix='stage')

    data_pre.to_csv('../notebooks/data/data-engineering.csv', index=False)
    return data_pre

