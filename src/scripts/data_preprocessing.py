import pandas as pd
from datetime import datetime
import numpy as np

def column_label_to_index(col_label):
    col_index = 0
    for c in col_label.upper():
        col_index = col_index * 26 + (ord(c) - ord('A') + 1)
    return col_index - 1


def add_prefix_to_first_row(dataframe, prefix, start_col_label, end_col_label):
    start_col = column_label_to_index(start_col_label)
    end_col = column_label_to_index(end_col_label)
    for col in range(start_col, end_col + 1):
        dataframe.iat[0, col] = prefix + dataframe.iat[0, col]

def mergeHeader_Columns(data):
    add_prefix_to_first_row(data, 'PESSOA_PIPEDRIVE_', 'A', 'R')
    add_prefix_to_first_row(data, 'FUNIL_ASSINATURA_PIPEDRIVE_', 'S', 'X')
    add_prefix_to_first_row(data, 'FUNIL_ONBOARDING_PIPEDRIVE_', 'Y', 'AH')
    add_prefix_to_first_row(data, 'ATENDIMENTOS_AGENDA_', 'AJ', 'AY')
    add_prefix_to_first_row(data, 'WHOQOL_', 'AZ', 'BD')
    add_prefix_to_first_row(data, 'COMUNICARE_', 'BE', 'BE')
    add_prefix_to_first_row(data, 'TWILIO_', 'BF', 'BM')
    add_prefix_to_first_row(data, 'COBRANÇA_VINDI_', 'BN', 'BU')

    data.columns = data.iloc[0]
    data = data.drop(data.index[0])
    return data

def preprocessing(data_dataframe):
    from sklearn.impute import SimpleImputer
    data_dataframe = mergeHeader_Columns(data_dataframe)
    # preprocessing 1
    data_dataframe = data_dataframe.drop(["PESSOA_PIPEDRIVE_id_person_recommendation","PESSOA_PIPEDRIVE_Recebe Comunicados?", "PESSOA_PIPEDRIVE_Interesses", "PESSOA_PIPEDRIVE_Pontos de Atenção", "FUNIL_ONBOARDING_PIPEDRIVE_id_label"], axis=1)

    data_dataframe['PESSOA_PIPEDRIVE_birthdate'] = pd.to_datetime(data_dataframe['PESSOA_PIPEDRIVE_birthdate'])
    data_dataframe['PESSOA_PIPEDRIVE_age'] = data_dataframe['PESSOA_PIPEDRIVE_birthdate'].apply(
        lambda x: datetime.today().year - x.year - ((datetime.today().month, datetime.today().day) < (x.month, x.day))
    )

    imputer = SimpleImputer(strategy='mean')
    data_dataframe['PESSOA_PIPEDRIVE_age'] = imputer.fit_transform(data_dataframe['PESSOA_PIPEDRIVE_age'].values.reshape(-1, 1))
    data_dataframe['PESSOA_PIPEDRIVE_age'] = np.round(data_dataframe['PESSOA_PIPEDRIVE_age']).astype(int)

    data_dataframe = data_dataframe.drop(['PESSOA_PIPEDRIVE_birthdate'], axis=1 )

    rows_to_drop = data_dataframe[data_dataframe["PESSOA_PIPEDRIVE_id_gender"].isin([117,110,111])]
    data_dataframe = data_dataframe.drop(rows_to_drop.index, axis=0)
    data_dataframe["PESSOA_PIPEDRIVE_id_gender"].fillna(64, inplace=True)
    data_dataframe["PESSOA_PIPEDRIVE_id_marrital_status"].fillna(80, inplace=True)

    
    data_dataframe["PESSOA_PIPEDRIVE_state"].fillna(data_dataframe["PESSOA_PIPEDRIVE_state"].mode()[0], inplace=True)


    data_dataframe["PESSOA_PIPEDRIVE_city"].fillna(data_dataframe["PESSOA_PIPEDRIVE_city"].mode()[0], inplace=True)


    # data_dataframe = data_dataframe.drop(["PESSOA_PIPEDRIVE_postal_code"], axis=1)

    data_dataframe['PESSOA_PIPEDRIVE_id_health_plan'].fillna(data_dataframe['PESSOA_PIPEDRIVE_id_health_plan'].mode()[0], inplace=True)
    data_dataframe['PESSOA_PIPEDRIVE_has_public_health_plan'] = data_dataframe['PESSOA_PIPEDRIVE_id_health_plan'].apply(lambda x: 1 if int(x) == 412 else 0)
    data_dataframe = data_dataframe.drop(['PESSOA_PIPEDRIVE_id_health_plan'], axis=1)
    data_dataframe["PESSOA_PIPEDRIVE_tem_data_dataframe_de_termino_de_contrato"] = data_dataframe["PESSOA_PIPEDRIVE_contract_end_date"].apply(lambda x: 0 if pd.isna(x) else 1)
    data_dataframe.drop(["PESSOA_PIPEDRIVE_id_continuity_pf"], axis=1, inplace=True)
    data_dataframe["PESSOA_PIPEDRIVE_Canal de Preferência"].fillna(0, inplace=True)
    data_dataframe["PESSOA_PIPEDRIVE_Tem_Canal_de_Preferência"] = data_dataframe["PESSOA_PIPEDRIVE_Canal de Preferência"].apply(lambda x: 1 if int(x) > 0  else 0)
    data_dataframe["PESSOA_PIPEDRIVE_has_notes"] = data_dataframe["PESSOA_PIPEDRIVE_notes_count"].apply(lambda x: 1 if int(x) > 0 else 0)
    
    # preprocessing 2
    data_dataframe = data_dataframe.drop(["ATENDIMENTOS_AGENDA_Faltas Psicoterapia","TWILIO_Ligações Inbound", "TWILIO_Data Última Ligações Inbound","COBRANÇA_VINDI_Qde Total de Faturas","COBRANÇA_VINDI_Qde Total de Tentativas de Cobrança","COBRANÇA_VINDI_Método de Pagamento","COBRANÇA_VINDI_Valor Médio da Mensalidade","COBRANÇA_VINDI_Qde Total de Faturas Pagas após Vencimento","COBRANÇA_VINDI_Qde Total de Faturas Inadimpletes","COBRANÇA_VINDI_Valor Total Inadimplência"], axis=1)

    data_dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia"].fillna(0, inplace=True)
    
    data_dataframe["ATENDIMENTOS_AGENDA_Datas Psicoterapia"] = pd.to_datetime(data_dataframe["ATENDIMENTOS_AGENDA_Datas Psicoterapia"])

    data_dataframe["ATENDIMENTOS_AGENDA_Datas Psicoterapia Tempo passado"] = datetime.now() - data_dataframe["ATENDIMENTOS_AGENDA_Datas Psicoterapia"]

    data_dataframe["ATENDIMENTOS_AGENDA_Datas Psicoterapia Tempo passado"].fillna('', inplace=True)

    data_dataframe["ATENDIMENTOS_AGENDA_Datas Psicoterapia Tempo passado"] = data_dataframe["ATENDIMENTOS_AGENDA_Datas Psicoterapia Tempo passado"].astype(str)

    data_dataframe["ATENDIMENTOS_AGENDA_Datas Psicoterapia Tempo passado"] = data_dataframe["ATENDIMENTOS_AGENDA_Datas Psicoterapia Tempo passado"].str.extract('(\d+) days').astype(float)

    data_dataframe["ATENDIMENTOS_AGENDA_Datas Psicoterapia Recente"] = data_dataframe["ATENDIMENTOS_AGENDA_Datas Psicoterapia Tempo passado"] < data_dataframe["ATENDIMENTOS_AGENDA_Datas Psicoterapia Tempo passado"].median()

    data_dataframe = data_dataframe.drop(columns="WHOQOL_Qde Respostas WHOQOL")

    data_dataframe["WHOQOL_Físico_New"] = data_dataframe["WHOQOL_Físico"].str.split(';').str[-1].str.strip()

    data_dataframe["WHOQOL_Físico_New"] = data_dataframe["WHOQOL_Físico_New"].str.replace(",",".")

    data_dataframe["WHOQOL_Físico_New"] = data_dataframe["WHOQOL_Físico_New"].astype(float) 

    data_dataframe["WHOQOL_Físico_New"] = data_dataframe["WHOQOL_Físico_New"].fillna(data_dataframe["WHOQOL_Físico_New"].median())

    data_dataframe["WHOQOL_Psicológico_New"] = data_dataframe["WHOQOL_Psicológico"].str.split(';').str[-1].str.strip()

    data_dataframe["WHOQOL_Psicológico_New"] = data_dataframe["WHOQOL_Psicológico_New"].str.replace(",",".")

    data_dataframe["WHOQOL_Psicológico_New"] = data_dataframe["WHOQOL_Psicológico_New"].astype(float) 

    data_dataframe["WHOQOL_Psicológico_New"] = data_dataframe["WHOQOL_Psicológico_New"].fillna(data_dataframe["WHOQOL_Psicológico_New"].median())

    data_dataframe["WHOQOL_Social_New"] = data_dataframe["WHOQOL_Social"].str.split(';').str[-1].str.strip()

    data_dataframe["WHOQOL_Social_New"] = data_dataframe["WHOQOL_Social_New"].str.replace(",",".")

    data_dataframe["WHOQOL_Social_New"] = data_dataframe["WHOQOL_Social_New"].astype(float) 

    data_dataframe["WHOQOL_Social_New"] = data_dataframe["WHOQOL_Social_New"].fillna(data_dataframe["WHOQOL_Social_New"].median())

    data_dataframe["WHOQOL_Ambiental_New"] = data_dataframe["WHOQOL_Ambiental"].str.split(';').str[-1].str.strip()

    data_dataframe["WHOQOL_Ambiental_New"] = data_dataframe["WHOQOL_Ambiental_New"].str.replace(",",".")

    data_dataframe["WHOQOL_Ambiental_New"] = data_dataframe["WHOQOL_Ambiental_New"].astype(float) 

    data_dataframe["WHOQOL_Ambiental_New"] = data_dataframe["WHOQOL_Ambiental_New"].fillna(data_dataframe["WHOQOL_Ambiental_New"].median())

    data_dataframe["COMUNICARE_Problemas Abertos Bool"] = data_dataframe["COMUNICARE_Problemas Abertos"].notnull().astype(int)

    data_dataframe["COMUNICARE_Problemas Abertos Bool"].fillna(0, inplace=True)

    data_dataframe["TWILIO_Mensagens Inbound"].fillna(0, inplace=True)

    data_dataframe["TWILIO_Data Última Mensagens Inbound"] = pd.to_datetime(data_dataframe["TWILIO_Data Última Mensagens Inbound"])

    data_dataframe["TWILIO_Data Última Mensagens Inbound Tempo Passado"] = datetime.now() - data_dataframe["TWILIO_Data Última Mensagens Inbound"]

    data_dataframe["TWILIO_Data Última Mensagens Inbound Tempo Passado"].fillna('', inplace=True)

    data_dataframe["TWILIO_Data Última Mensagens Inbound Tempo Passado"] = data_dataframe["TWILIO_Data Última Mensagens Inbound Tempo Passado"].astype(str)

    data_dataframe["TWILIO_Data Última Mensagens Inbound Tempo Passado"] = data_dataframe["TWILIO_Data Última Mensagens Inbound Tempo Passado"].str.extract('(\d+) days').astype(float)

    data_dataframe["TWILIO_Data Última Mensagens Inbound Recente"] = data_dataframe["TWILIO_Data Última Mensagens Inbound Tempo Passado"] < data_dataframe["TWILIO_Data Última Mensagens Inbound Tempo Passado"].median()

    data_dataframe = data_dataframe.drop(columns=["WHOQOL_Ambiental","WHOQOL_Social","WHOQOL_Físico","WHOQOL_Psicológico","COMUNICARE_Problemas Abertos","TWILIO_Data Última Mensagens Inbound","ATENDIMENTOS_AGENDA_Datas Psicoterapia","ATENDIMENTOS_AGENDA_Datas Psicoterapia Tempo passado","TWILIO_Data Última Mensagens Inbound Tempo Passado"])
    

    # preprocessing 3

    # preprocessing 4
   
    data_dataframe["TWILIO_Mensagens Outbound"].fillna(0, inplace=True)

    data_dataframe["TWILIO_Data Última Mensagens Outbound"] = pd.to_datetime(data_dataframe["TWILIO_Data Última Mensagens Outbound"])

    data_dataframe["TWILIO_Data Última Mensagens Outbound Tempo passado"] = datetime.now() - data_dataframe["TWILIO_Data Última Mensagens Outbound"]

    data_dataframe["TWILIO_Data Última Mensagens Outbound Tempo passado"].fillna('', inplace=True)
    
    data_dataframe["TWILIO_Data Última Mensagens Outbound Tempo passado"] = data_dataframe["TWILIO_Data Última Mensagens Outbound Tempo passado"].astype(str)

    data_dataframe["TWILIO_Data Última Mensagens Outbound Tempo passado"] = data_dataframe["TWILIO_Data Última Mensagens Outbound Tempo passado"].str.extract('(\d+) days').astype(float)

    data_dataframe = data_dataframe.drop(["TWILIO_Data Última Mensagens Outbound"], axis=1)

    data_dataframe["TWILIO_Data Última Mensagens Outbound Recente"] = data_dataframe["TWILIO_Data Última Mensagens Outbound Tempo passado"] < data_dataframe["TWILIO_Data Última Mensagens Outbound Tempo passado"].median()

    data_dataframe = data_dataframe.drop(["TWILIO_Data Última Mensagens Outbound Tempo passado"], axis=1)

    data_dataframe["TWILIO_Ligações Outbound"].fillna(0, inplace=True)

    data_dataframe["TWILIO_Data Última Ligações Outbound"] = pd.to_datetime(data_dataframe["TWILIO_Data Última Ligações Outbound"])

    data_dataframe["TWILIO_Data Última Ligações Outbound Tempo passado"] = datetime.now() - data_dataframe["TWILIO_Data Última Ligações Outbound"]

    data_dataframe["TWILIO_Data Última Ligações Outbound Tempo passado"].fillna('', inplace=True)

    data_dataframe["TWILIO_Data Última Ligações Outbound Tempo passado"] = data_dataframe["TWILIO_Data Última Ligações Outbound Tempo passado"].astype(str)

    data_dataframe["TWILIO_Data Última Ligações Outbound Tempo passado"] = data_dataframe["TWILIO_Data Última Ligações Outbound Tempo passado"].str.extract('(\d+) days').astype(float)

    data_dataframe = data_dataframe.drop(["TWILIO_Data Última Ligações Outbound"], axis=1)

    data_dataframe["TWILIO_Data Última Ligações Outbound Recente"] = data_dataframe["TWILIO_Data Última Ligações Outbound Tempo passado"] < data_dataframe["TWILIO_Data Última Ligações Outbound Tempo passado"].median()

    data_dataframe = data_dataframe.drop(["TWILIO_Data Última Ligações Outbound Tempo passado"], axis=1)

    data_dataframe = data_dataframe.drop(["COBRANÇA_VINDI_Qde Perfis de Pagamento Inativos"], axis=1)

    # preprocessing especials 

    data_dataframe = data_dataframe[data_dataframe['FUNIL_ASSINATURA_PIPEDRIVE_status'].isin(['won', 'lost'])]

    data_dataframe = data_dataframe.drop(data_dataframe[(data_dataframe['FUNIL_ASSINATURA_PIPEDRIVE_status'] == 'won') & (~data_dataframe['PESSOA_PIPEDRIVE_contract_end_date'].isnull())].index)

    data_dataframe = data_dataframe.drop(data_dataframe[(data_dataframe['FUNIL_ASSINATURA_PIPEDRIVE_status'] == 'lost') & (data_dataframe['PESSOA_PIPEDRIVE_contract_end_date'].isnull())].index)

    return data_dataframe






