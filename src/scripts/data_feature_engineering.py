import pandas as pd
from category_encoders import CountEncoder

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


    for indice, valor in dataframe['FUNIL_ASSINATURA_PIPEDRIVE_start_of_service'].items():
        if pd.isnull(valor):
            dataframe.loc[indice, 'FUNIL_ASSINATURA_PIPEDRIVE_start_of_service'] = dataframe.loc[indice, 'PESSOA_PIPEDRIVE_contract_start_date']

    lost_reason_dummies = pd.get_dummies(dataframe['FUNIL_ASSINATURA_PIPEDRIVE_lost_reason'], prefix='lost_reason')
    dataframe = pd.concat([dataframe, lost_reason_dummies], axis=1)

    data_status_encoded = pd.get_dummies(dataframe['FUNIL_ONBOARDING_PIPEDRIVE_status'], prefix='Status')
    dataframe = pd.concat([dataframe, data_status_encoded], axis=1)

    lost_reason_dummies = pd.get_dummies(dataframe['FUNIL_ONBOARDING_PIPEDRIVE_lost_reason'], prefix='lost_reason')
    dataframe = pd.concat([dataframe, lost_reason_dummies], axis=1)

    dataframe.drop('ATENDIMENTOS_AGENDA_Qde Todos Atendimentos', axis='columns', inplace=True)

    




