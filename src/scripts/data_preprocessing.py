import pandas as pd
from datetime import datetime
import numpy as np
import datetime as dt

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
    add_prefix_to_first_row(data, 'ATENDIMENTOS_AGENDA_', 'AI', 'AU')
    add_prefix_to_first_row(data, 'WHOQOL_', 'AV', 'AZ')
    add_prefix_to_first_row(data, 'COMUNICARE_', 'BA', 'BA')
    add_prefix_to_first_row(data, 'TWILIO_', 'BB', 'BI')
    add_prefix_to_first_row(data, 'COBRANÇA_VINDI_', 'BJ', 'BQ')

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

    data_dataframe = data_dataframe.drop(columns=["WHOQOL_Ambiental","WHOQOL_Social","WHOQOL_Físico","WHOQOL_Psicológico","COMUNICARE_Problemas Abertos","TWILIO_Data Última Mensagens Inbound","ATENDIMENTOS_AGENDA_Datas Psicoterapia","TWILIO_Data Última Mensagens Inbound Tempo Passado"])
    
    # preprocessing 3
    for indice, valor in data_dataframe["FUNIL_ASSINATURA_PIPEDRIVE_lost_time"].items():
        if pd.notna(valor) == False: 
            if pd.notna(data_dataframe.loc[indice, "PESSOA_PIPEDRIVE_contract_end_date"]):
                data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"] = data_dataframe.loc[indice, "PESSOA_PIPEDRIVE_contract_end_date"]

    data_dataframe["FUNIL_ASSINATURA_PIPEDRIVE_lost_time"].fillna(dt.date.today(), inplace=True)

    for indice, valor in data_dataframe["FUNIL_ASSINATURA_PIPEDRIVE_lost_time"].items():
        index = str(data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"]).find(";")
        if index != -1:
            data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"] = data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"][:index]

    for indice, valor in data_dataframe["FUNIL_ASSINATURA_PIPEDRIVE_lost_time"].items():
        tamanho = len(str(data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"]))
        if tamanho > 10:
            data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"] = data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"][:10]	

    for indice, valor in data_dataframe["FUNIL_ASSINATURA_PIPEDRIVE_lost_time"].items():
        data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"] = pd.to_datetime(data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"], format='%Y-%m-%d', errors='coerce')
        data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"] = data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"].strftime('%Y-%m-%d')

    tempo_permanencia = []

    for indice, valor in data_dataframe["FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"].items():
        if pd.notna(valor):
            index = data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"].find(";")
            if index != -1:
                data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"] = data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"][:index]

    for indice, valor in data_dataframe["FUNIL_ASSINATURA_PIPEDRIVE_lost_time"].items():
        if pd.notna(data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"]):
            tempo_1 = datetime.strptime(data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"], '%Y-%m-%d')
            tempo_2 = datetime.strptime(data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"], '%Y-%m-%d')
            tempo_permanencia.append(str(tempo_1 - tempo_2))
        else:
            tempo_1 = datetime.strptime(data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"], '%Y-%m-%d')
            tempo_2 = datetime.strptime(data_dataframe.loc[indice, "PESSOA_PIPEDRIVE_contract_start_date"], '%Y-%m-%d')
            tempo_permanencia.append(str(tempo_1 - tempo_2))

    data_dataframe['stay_time'] = tempo_permanencia

    for indice, valor in data_dataframe["stay_time"].items():
        index = data_dataframe.loc[indice, "stay_time"].find(",")
        if index != -1:
            data_dataframe.loc[indice, "stay_time"] = data_dataframe.loc[indice, "stay_time"][:index]

    for indice, valor in data_dataframe["FUNIL_ASSINATURA_PIPEDRIVE_lost_reason"].items():
        if pd.notna(valor):  
            index = data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_reason"].find(";")
            if index != -1: 
                data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_reason"] = data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_reason"][:index]
        else:
            data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_reason"] = "Assinatura ativa"
            
        contagem = data_dataframe["FUNIL_ASSINATURA_PIPEDRIVE_lost_reason"].value_counts()

        agrupamento = contagem[contagem < 20].index
        data_dataframe.loc[data_dataframe["FUNIL_ASSINATURA_PIPEDRIVE_lost_reason"].isin(agrupamento), "FUNIL_ASSINATURA_PIPEDRIVE_lost_reason"] = "Outro"

    data_dataframe['FUNIL_ONBOARDING_PIPEDRIVE_add_time'].fillna('Não iniciado', inplace=True)

    ultimos_estados = []

    for indice, valor in data_dataframe["FUNIL_ONBOARDING_PIPEDRIVE_add_time"].items():
        if valor != "Não iniciado":
            if pd.notna(data_dataframe.loc[indice, "FUNIL_ONBOARDING_PIPEDRIVE_stay_in_pipeline_stages_welcome"]):
                if pd.notna(data_dataframe.loc[indice, "FUNIL_ONBOARDING_PIPEDRIVE_stay_in_pipeline_stages_first_meeting"]):
                    if pd.notna(data_dataframe.loc[indice, "FUNIL_ONBOARDING_PIPEDRIVE_stay_in_pipeline_stages_whoqol"]):
                        ultimos_estados.append("Questionário")
                    else:
                        ultimos_estados.append("Primeira reunião")
                else:
                    ultimos_estados.append("Boas-vindas")
            
        else:
            ultimos_estados.append("Não iniciado")

    data_dataframe["last_stage_concluded"] = ultimos_estados

    data_dataframe.drop(["FUNIL_ONBOARDING_PIPEDRIVE_stay_in_pipeline_stages_welcome", "FUNIL_ONBOARDING_PIPEDRIVE_stay_in_pipeline_stages_first_meeting", "FUNIL_ONBOARDING_PIPEDRIVE_stay_in_pipeline_stages_whoqol"], axis=1, inplace=True)

    data_dataframe["FUNIL_ONBOARDING_PIPEDRIVE_status"].fillna("Não iniciado", inplace=True)

    tempo = []

    for indice, valor in data_dataframe["FUNIL_ONBOARDING_PIPEDRIVE_add_time"].items():
        if valor != "Não iniciado":
            if pd.notna(data_dataframe.loc[indice, "FUNIL_ONBOARDING_PIPEDRIVE_lost_time"]) == True:
                tempo.append(data_dataframe.loc[indice, "FUNIL_ONBOARDING_PIPEDRIVE_lost_time"])
            elif pd.notna(data_dataframe.loc[indice, "FUNIL_ONBOARDING_PIPEDRIVE_won_time"]) == True:
                tempo.append(data_dataframe.loc[indice, "FUNIL_ONBOARDING_PIPEDRIVE_won_time"])
            else:
                tempo.append("Em aberto")
        else:
            tempo.append("Não iniciado")

    data_dataframe['process_time'] = tempo

    data_dataframe.drop(["FUNIL_ONBOARDING_PIPEDRIVE_won_time", "FUNIL_ONBOARDING_PIPEDRIVE_lost_time"], axis=1, inplace=True)

    data_dataframe["FUNIL_ONBOARDING_PIPEDRIVE_activities_count"] = data_dataframe["FUNIL_ONBOARDING_PIPEDRIVE_activities_count"].fillna(0)

    data_dataframe["ATENDIMENTOS_AGENDA_Qde Atendimento Médico"] = data_dataframe["ATENDIMENTOS_AGENDA_Qde Atendimento Médico"].fillna(0)

    data_dataframe["ATENDIMENTOS_AGENDA_Faltas Atendimento Médico"] = data_dataframe["ATENDIMENTOS_AGENDA_Faltas Atendimento Médico"].fillna(0)

    data_dataframe["ATENDIMENTOS_AGENDA_Datas Atendimento Médico"] = data_dataframe["ATENDIMENTOS_AGENDA_Datas Atendimento Médico"].fillna("Nunca ocorreu")

    for indice, valor in data_dataframe["FUNIL_ONBOARDING_PIPEDRIVE_lost_reason"].items():
        if pd.notna(valor) == False:
            if pd.notna(data_dataframe.loc[indice, "FUNIL_ONBOARDING_PIPEDRIVE_status"]) == False and pd.notna(data_dataframe.loc[indice, "FUNIL_ONBOARDING_PIPEDRIVE_add_time"]):
                data_dataframe.loc[indice, "FUNIL_ONBOARDING_PIPEDRIVE_lost_reason"] = "Processo em aberto"
            if data_dataframe.loc[indice, "FUNIL_ONBOARDING_PIPEDRIVE_status"] == "won":
                data_dataframe.loc[indice, "FUNIL_ONBOARDING_PIPEDRIVE_lost_reason"] = "Processo concluído"
            else:
                data_dataframe.loc[indice, "FUNIL_ONBOARDING_PIPEDRIVE_lost_reason"] = "Processo não iniciado"

        contagem = data_dataframe["FUNIL_ONBOARDING_PIPEDRIVE_lost_reason"].value_counts()

        agrupamento = contagem[contagem < 23].index
        data_dataframe.loc[data_dataframe["FUNIL_ONBOARDING_PIPEDRIVE_lost_reason"].isin(agrupamento), "FUNIL_ONBOARDING_PIPEDRIVE_lost_reason"] = "Outro"

    data_dataframe["ATENDIMENTOS_AGENDA_Qde Atendimentos Acolhimento"] = data_dataframe["ATENDIMENTOS_AGENDA_Qde Atendimentos Acolhimento"].fillna(0)

    data_dataframe["ATENDIMENTOS_AGENDA_Faltas Acolhimento"] = data_dataframe["ATENDIMENTOS_AGENDA_Faltas Acolhimento"].fillna(0)

    data_dataframe["ATENDIMENTOS_AGENDA_Datas Acolhimento"] = data_dataframe["ATENDIMENTOS_AGENDA_Datas Acolhimento"].fillna("Nunca ocorreu")

    data_dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia"] = data_dataframe["ATENDIMENTOS_AGENDA_Qde Psicoterapia"].fillna(0)

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

    #exportando df pronto

    data_dataframe.to_csv('data-preprocessed.csv', index=False)

    return data_dataframe

preprocessing(pd.read_csv('../notebooks/data/data.csv'))