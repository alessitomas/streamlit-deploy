import pandas as pd
from datetime import datetime

def preprocessing(data_dataframe):
    # preprocessing 1
    data_dataframe = data_dataframe.drop(["PESSOA_PIPEDRIVE_id_person_recommendation","PESSOA_PIPEDRIVE_Recebe Comunicados?", "PESSOA_PIPEDRIVE_Interesses", "PESSOA_PIPEDRIVE_Pontos de Atenção", "FUNIL_ONBOARDING_PIPEDRIVE_id_label"], axis=1)

    # preprocessing 2
    data_dataframe = data_dataframe.drop(["ATENDIMENTOS_AGENDA_Faltas Psicoterapia","TWILIO_Ligações Inbound", "TWILIO_Data Última Ligações Inbound","COBRANÇA_VINDI_Qde Total de Faturas","COBRANÇA_VINDI_Qde Total de Tentativas de Cobrança","COBRANÇA_VINDI_Método de Pagamento","COBRANÇA_VINDI_Valor Médio da Mensalidade","COBRANÇA_VINDI_Qde Total de Faturas Pagas após Vencimento","COBRANÇA_VINDI_Qde Total de Faturas Inadimpletes","COBRANÇA_VINDI_Valor Total Inadimplência"], axis=1)

    data_dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia"].fillna(0)
    
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

    data_dataframe["COMUNICARE_Problemas Abertos Bool"].fillna(0)

    data_dataframe["TWILIO_Mensagens Inbound"].fillna(0)

    data_dataframe["TWILIO_Data Última Mensagens Inbound"] = pd.to_datetime(data_dataframe["TWILIO_Data Última Mensagens Inbound"])

    data_dataframe["TWILIO_Data Última Mensagens Inbound Tempo Passado"] = datetime.now() - data_dataframe["TWILIO_Data Última Mensagens Inbound"]

    data_dataframe["TWILIO_Data Última Mensagens Inbound Tempo Passado"].fillna('', inplace=True)

    data_dataframe["TWILIO_Data Última Mensagens Inbound Tempo Passado"] = data_dataframe["TWILIO_Data Última Mensagens Inbound Tempo Passado"].astype(str)

    data_dataframe["TWILIO_Data Última Mensagens Inbound Tempo Passado"] = data_dataframe["TWILIO_Data Última Mensagens Inbound Tempo Passado"].str.extract('(\d+) days').astype(float)

    data_dataframe["TWILIO_Data Última Mensagens Inbound Recente"] = data_dataframe["TWILIO_Data Última Mensagens Inbound Tempo Passado"] < data_dataframe["TWILIO_Data Última Mensagens Inbound Tempo Passado"].median()

    data_dataframe = data_dataframe.drop(columns=["WHOQOL_Ambiental","WHOQOL_Social","WHOQOL_Físico","WHOQOL_Psicológico","COMUNICARE_Problemas Abertos","TWILIO_Data Última Mensagens Inbound","ATENDIMENTOS_AGENDA_Datas Psicoterapia","ATENDIMENTOS_AGENDA_Datas Psicoterapia Tempo passado","TWILIO_Data Última Mensagens Inbound Tempo Passado"])
    

    # preprocessing 3

    # preprocessing 4
    data_dataframe = data_dataframe.drop(["ATENDIMENTOS_AGENDA_Faltas Psicoterapia","TWILIO_Ligações Inbound", "TWILIO_Data Última Ligações Inbound","COBRANÇA_VINDI_Qde Total de Faturas","COBRANÇA_VINDI_Qde Total de Tentativas de Cobrança","COBRANÇA_VINDI_Método de Pagamento","COBRANÇA_VINDI_Valor Médio da Mensalidade","COBRANÇA_VINDI_Qde Total de Faturas Pagas após Vencimento","COBRANÇA_VINDI_Qde Total de Faturas Inadimpletes","COBRANÇA_VINDI_Valor Total Inadimplência"], axis=1)

    data_dataframe["TWILIO_Mensagens Outbound"].fillna(0)

    data_dataframe["TWILIO_Data Última Mensagens Outbound"] = pd.to_datetime(data_dataframe["TWILIO_Data Última Mensagens Outbound"])

    data_dataframe["TWILIO_Data Última Mensagens Outbound Tempo passado"] = datetime.now() - data_dataframe["TWILIO_Data Última Mensagens Outbound"]

    data_dataframe["TWILIO_Data Última Mensagens Outbound Tempo passado"].fillna('', inplace=True)
    
    data_dataframe["TWILIO_Data Última Mensagens Outbound Tempo passado"] = data_dataframe["TWILIO_Data Última Mensagens Outbound Tempo passado"].astype(str)

    data_dataframe["TWILIO_Data Última Mensagens Outbound Tempo passado"] = data_dataframe["TWILIO_Data Última Mensagens Outbound Tempo passado"].str.extract('(\d+) days').astype(float)

    data_dataframe = data_dataframe.drop(["TWILIO_Data Última Mensagens Outbound"], axis=1)

    data_dataframe["TWILIO_Data Última Mensagens Outbound Recente"] = data_dataframe["TWILIO_Data Última Mensagens Outbound Tempo passado"] < data_dataframe["TWILIO_Data Última Mensagens Outbound Tempo passado"].median()

    data_dataframe = data_dataframe.drop(["TWILIO_Data Última Mensagens Outbound Tempo passado"], axis=1)

    data_dataframe["TWILIO_Ligações Outbound"].fillna(0)

    data_dataframe["TWILIO_Data Última Ligações Outbound"] = pd.to_datetime(data_dataframe["TWILIO_Data Última Ligações Outbound"])

    data_dataframe["TWILIO_Data Última Ligações Outbound Tempo passado"] = datetime.now() - data_dataframe["TWILIO_Data Última Ligações Outbound"]

    data_dataframe["TWILIO_Data Última Ligações Outbound Tempo passado"].fillna('', inplace=True)

    data_dataframe["TWILIO_Data Última Ligações Outbound Tempo passado"] = data_dataframe["TWILIO_Data Última Ligações Outbound Tempo passado"].astype(str)

    data_dataframe["TWILIO_Data Última Ligações Outbound Tempo passado"] = data_dataframe["TWILIO_Data Última Ligações Outbound Tempo passado"].str.extract('(\d+) days').astype(float)

    data_dataframe = data_dataframe.drop(["TWILIO_Data Última Ligações Outbound"], axis=1)

    data_dataframe["TWILIO_Data Última Ligações Outbound Recente"] = data_dataframe["TWILIO_Data Última Ligações Outbound Tempo passado"] < data_dataframe["TWILIO_Data Última Ligações Outbound Tempo passado"].median()

    data_dataframe = data_dataframe.drop(["TWILIO_Data Última Ligações Outbound Tempo passado"], axis=1)

    data_dataframe = data_dataframe.drop(["COBRANÇA_VINDI_Qde Perfis de Pagamento Inativos"], axis=1)

    return data_dataframe