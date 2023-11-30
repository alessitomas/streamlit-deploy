import pandas as pd
import numpy as np
from category_encoders import CountEncoder
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from scipy import stats
from sklearn.utils import resample


def feature_engineering(dataframe):

    # feature engineering 1 + 3

    dataframe["stay_time"] = dataframe["stay_time"].str.extract('(\d+) days').astype(float)

    dataframe["stay_time"].fillna(0,inplace=True)

    dataframe["ATENDIMENTOS_AGENDA_Qde Atendimentos Acolhimento"].fillna(0,inplace=True)
    dataframe["ATENDIMENTOS_AGENDA_Faltas Acolhimento"].fillna(0,inplace=True)
    dataframe["ATENDIMENTOS_AGENDA_Datas Acolhimento"].fillna("Nunca ocorreu",inplace=True)
    dataframe = dataframe[~dataframe['ATENDIMENTOS_AGENDA_Datas Acolhimento'].astype(str).str.contains("Nunca ocorreu")]
    # Suponha que você tenha um DataFrame chamado 'data' com uma coluna 'ATENDIMENTOS_AGENDA_Datas Acolhimento'
    dataframe['ATENDIMENTOS_AGENDA_Datas Acolhimento'] = dataframe['ATENDIMENTOS_AGENDA_Datas Acolhimento'].str.split(';')

    # Se você deseja criar uma nova coluna para cada data:
    dataframe = dataframe.explode('ATENDIMENTOS_AGENDA_Datas Acolhimento')
    dataframe['ATENDIMENTOS_AGENDA_Datas Acolhimento'] = pd.to_datetime(dataframe['ATENDIMENTOS_AGENDA_Datas Acolhimento'].str.strip(), format='%Y-%m-%d %H:%M:%S')
    dataframe['ATENDIMENTOS_AGENDA_Datas Acolhimento Por Mes'] = dataframe['ATENDIMENTOS_AGENDA_Datas Acolhimento'].dt.month
    atendimentos_por_mes = dataframe.groupby(['PESSOA_PIPEDRIVE_id_person', 'ATENDIMENTOS_AGENDA_Datas Acolhimento Por Mes']).size().reset_index(name='ATENDIMENTOS_AGENDA_Qde Atendimentos Acolhimento')
    dataframe = pd.merge(dataframe, atendimentos_por_mes, on=['PESSOA_PIPEDRIVE_id_person', 'ATENDIMENTOS_AGENDA_Datas Acolhimento Por Mes'], how='left')
    dataframe["ATENDIMENTOS_AGENDA_Faltas Taxa"] = dataframe["ATENDIMENTOS_AGENDA_Faltas Acolhimento"] / dataframe["ATENDIMENTOS_AGENDA_Qde Atendimentos Acolhimento_x"]
    dataframe["TWILIO_Mensagens Já Enviou"] = dataframe["TWILIO_Mensagens Inbound"] > 0
    dataframe["TWILIO_Mensagens Razão"] = dataframe["TWILIO_Mensagens Outbound"] / dataframe["TWILIO_Mensagens Inbound"].where(dataframe["TWILIO_Mensagens Já Enviou"], 1)
    dataframe["PESSOA_PIPEDRIVE CRIANÇA"] = dataframe["PESSOA_PIPEDRIVE_age"] <= 16
    dataframe["PESSOA_PIPEDRIVE JOVEM"] = (dataframe["PESSOA_PIPEDRIVE_age"] > 16) & (dataframe["PESSOA_PIPEDRIVE_age"] <= 30)
    dataframe["PESSOA_PIPEDRIVE ADULTO"] = (dataframe["PESSOA_PIPEDRIVE_age"] > 30) & (dataframe["PESSOA_PIPEDRIVE_age"] <= 60)
    dataframe["PESSOA_PIPEDRIVE IDOSO"] = dataframe["PESSOA_PIPEDRIVE_age"] > 60
    dataframe["TWILIO_Ligações Outbound Qtd Significativa"] = dataframe["TWILIO_Ligações Outbound"] >= dataframe["TWILIO_Ligações Outbound"].mean()
    dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia Nenhum"] = dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia"] == 0
    dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia Pouco"] = (dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia"] > 0) & (dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia"] <= dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia"].mean() )
    dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia Muito"] = dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia"] > dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia"].mean() 
    dataframe["ATENDIMENTOS_AGENDA_Qde Prescrições"].fillna(0,inplace=True)

    dataframe = dataframe.drop(["ATENDIMENTOS_AGENDA_Datas Prescrição"],axis=1)

    dataframe = dataframe[dataframe["PESSOA_PIPEDRIVE_id_gender"].isin([64,63])]   
    dataframe["PESSOA_PIPEDRIVE_id_gender Binário"] = dataframe["PESSOA_PIPEDRIVE_id_gender"].map({64: 0, 63: 1})
    dataframe = pd.get_dummies(dataframe, columns=['PESSOA_PIPEDRIVE_id_marrital_status'], prefix='Status')
    dataframe = pd.get_dummies(dataframe, columns=['PESSOA_PIPEDRIVE_state'], prefix='Estado')

    ce = CountEncoder()
    dataframe['PESSOA_PIPEDRIVE_city Codificada'] = ce.fit_transform(dataframe['PESSOA_PIPEDRIVE_city'])

    dataframe = dataframe.drop(columns=["PESSOA_PIPEDRIVE_city","PESSOA_PIPEDRIVE_id_gender"])
    dataframe = dataframe.drop(columns=["PESSOA_PIPEDRIVE_postal_code","PESSOA_PIPEDRIVE_id_person"])

    dataframe["PESSOA_PIPEDRIVE_contract_start_date"] = pd.to_datetime(dataframe["PESSOA_PIPEDRIVE_contract_start_date"], format='%Y-%m-%d')


    # feature engineering 2 + 3

    one_hot_encoded = pd.get_dummies(dataframe['FUNIL_ASSINATURA_PIPEDRIVE_status'], prefix='status')
    dataframe = pd.concat([dataframe, one_hot_encoded], axis=1)

    dataframe['FUNIL_ASSINATURA_PIPEDRIVE_start_of_service'] = pd.to_datetime(dataframe['FUNIL_ASSINATURA_PIPEDRIVE_start_of_service'])


    # for indice, valor in dataframe['FUNIL_ASSINATURA_PIPEDRIVE_start_of_service'].items():
    #     if pd.isnull(valor):
    #         dataframe.loc[indice, 'FUNIL_ASSINATURA_PIPEDRIVE_start_of_service'] = dataframe.loc[indice, 'PESSOA_PIPEDRIVE_contract_start_date']

    lost_reason_dummies = pd.get_dummies(dataframe['FUNIL_ASSINATURA_PIPEDRIVE_lost_reason'], prefix='lost_reason')
    dataframe = pd.concat([dataframe, lost_reason_dummies], axis=1)

    data_status_encoded = pd.get_dummies(dataframe['FUNIL_ONBOARDING_PIPEDRIVE_status'], prefix='Status')
    dataframe = pd.concat([dataframe, data_status_encoded], axis=1)

    lost_reason_dummies = pd.get_dummies(dataframe['FUNIL_ONBOARDING_PIPEDRIVE_lost_reason'], prefix='lost_reason')
    dataframe = pd.concat([dataframe, lost_reason_dummies], axis=1)

    dataframe.drop('ATENDIMENTOS_AGENDA_Qde Todos Atendimentos', axis='columns', inplace=True)



    # feature engineering 4 + 3

    
    # Tratar valores ausentes
    # for column in dataframe.columns:
    #     if dataframe[column].isnull().sum() > 0:
    #         if dataframe[column].dtype == np.number:
    #             dataframe[column].fillna(dataframe[column].median(), inplace=True)
    #         else:
    #             dataframe[column].fillna(dataframe[column].mode()[0], inplace=True)

    # Verificando se é categórica ou numérica
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

    # Convertendo a coluna 'process_time' para datetime e tratando valores inválidos
    # dataframe['process_time'] = pd.to_datetime(dataframe['process_time'], errors='coerce')

    # # Defina a data de referência adequada (substitua 'data_de_referencia' pela data real)
    # data_de_referencia = pd.to_datetime('2022-01-01')

    # # Calculando o tempo decorrido em dias desde a data de referência
    # dataframe['days_since_reference_date'] = (dataframe['process_time'] - data_de_referencia).dt.days

    # dataframe.dropna(subset=['days_since_reference_date'], inplace=True)

    # dataframe['TWILIO_Data Última Ligações Outbound Recente_Boolean_Numeric'] = dataframe['TWILIO_Data Última Ligações Outbound Recente'].astype(int)
   
    # # Verificando a distribuição da variável convertida
    # distribution = dataframe['TWILIO_Data Última Ligações Outbound Recente'].value_counts(normalize=True)

    # # Reamostragem para equilibrar as classes (se necessário)
    # # Este exemplo aumenta a classe minoritária (True/1)
    # class_0 = dataframe[dataframe['TWILIO_Data Última Ligações Outbound Recente_Boolean_Numeric'] == 0]
    # class_1 = dataframe[dataframe['TWILIO_Data Última Ligações Outbound Recente_Boolean_Numeric'] == 1]

    # # Checando se o balanceamento é necessário
    # if distribution.min() < 0.4:  # Supondo um limite de 40% para desequilíbrio
    #     class_1_upsampled = resample(class_1,
    #                                 replace=True,     # amostra com substituição
    #                                 n_samples=len(class_0),    # para igualar com a classe majoritária
    #                                 random_state=123) # seed para reprodutibilidade

    #     # Combinando a classe majoritária com a classe minoritária reamostrada
    #     dataframe = pd.concat([class_0, class_1_upsampled])


    dataframe.to_csv('data-engineering.csv', index=False)

    return dataframe


    
feature_engineering(pd.read_csv("data-preprocessed.csv"))



