import pandas as pd
from datetime import datetime

def preprocessing(data_dataframe):
    # preprocessing 1
    data_dataframe = data_dataframe.drop(["PESSOA_PIPEDRIVE_id_person_recommendation","PESSOA_PIPEDRIVE_Recebe Comunicados?", "PESSOA_PIPEDRIVE_Interesses", "PESSOA_PIPEDRIVE_Pontos de Atenção", "FUNIL_ONBOARDING_PIPEDRIVE_id_label"], axis=1)
    # preprocessing 2
    data_dataframe = data_dataframe.drop(["ATENDIMENTOS_AGENDA_Faltas Psicoterapia","TWILIO_Ligações Inbound", "TWILIO_Data Última Ligações Inbound","COBRANÇA_VINDI_Qde Total de Faturas","COBRANÇA_VINDI_Qde Total de Tentativas de Cobrança","COBRANÇA_VINDI_Método de Pagamento","COBRANÇA_VINDI_Valor Médio da Mensalidade","COBRANÇA_VINDI_Qde Total de Faturas Pagas após Vencimento","COBRANÇA_VINDI_Qde Total de Faturas Inadimpletes","COBRANÇA_VINDI_Valor Total Inadimplência"], axis=1)
    
     # preprocessing 3
    for indice, valor in data_dataframe["FUNIL_ASSINATURA_PIPEDRIVE_lost_time"].items():
        if pd.notna(valor) == False: 
            if pd.notna(data_dataframe.loc[indice, "PESSOA_PIPEDRIVE_contract_end_date"]):
                data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"] =  data_dataframe.loc[indice, "PESSOA_PIPEDRIVE_contract_end_date"]
            else:
                data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"] = "Em aberto"

    for indice, valor in data_dataframe["FUNIL_ASSINATURA_PIPEDRIVE_lost_time"].items():
        if data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"] != "Em aberto":
            index = data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"].find(";")
            if index != -1:
                data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"] = data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"][:index]

    for indice, valor in data_dataframe["FUNIL_ASSINATURA_PIPEDRIVE_lost_time"].items():
        if data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"] != "Em aberto":
            tamanho = len(data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"])
            if tamanho > 10:
                data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"] = data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"][:10]	

    tempo_permanencia = []

    for indice, valor in data_dataframe["FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"].items():
        if pd.notna(valor):
            index = data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"].find(";")
            if index != -1:
                data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"] = data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"][:index]

    for indice, valor in data_dataframe["FUNIL_ASSINATURA_PIPEDRIVE_lost_time"].items():
        if pd.notna(valor):
            if data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"] != "Em aberto":	
                if pd.notna(data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"]):
                    tempo_1 = datetime.strptime(data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"], '%Y-%m-%d')
                    tempo_2 = datetime.strptime(data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_start_of_service"], '%Y-%m-%d')
                    tempo_permanencia.append(str(tempo_1 - tempo_2))
                else:
                    tempo_1 = datetime.strptime(data_dataframe.loc[indice, "FUNIL_ASSINATURA_PIPEDRIVE_lost_time"], '%Y-%m-%d')
                    tempo_2 = datetime.strptime(data_dataframe.loc[indice, "PESSOA_PIPEDRIVE_contract_start_date"], '%Y-%m-%d')
                    tempo_permanencia.append(str(tempo_1 - tempo_2))
            else:
                tempo_permanencia.append("Em aberto")

    data_dataframe['stay_time'] = tempo_permanencia

    for indice, valor in data_dataframe["stay_time"].items():
        if valor != "Em aberto":
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

    data_dataframe["process_time"].to_csv('data/data2q.csv', sep=';', index=False)

    data_dataframe.drop(["FUNIL_ONBOARDING_PIPEDRIVE_won_time", "FUNIL_ONBOARDING_PIPEDRIVE_lost_time"], axis=1, inplace=True)

    data_dataframe["FUNIL_ONBOARDING_PIPEDRIVE_activities_count"] = data_dataframe["FUNIL_ONBOARDING_PIPEDRIVE_activities_count"].fillna(0)

    data_dataframe["ATENDIMENTOS_AGENDA_Qde Atendimento Médico"] = data_dataframe["ATENDIMENTOS_AGENDA_Qde Atendimento Médico"].fillna(0)

    data_dataframe["ATENDIMENTOS_AGENDA_Faltas Atendimento Médico"] = data_dataframe["ATENDIMENTOS_AGENDA_Faltas Atendimento Médico"].fillna(0)

    data_dataframe["ATENDIMENTOS_AGENDA_Datas Atendimento Médico"] = data_dataframe["ATENDIMENTOS_AGENDA_Datas Atendimento Médico"].fillna("Nunca ocorreu")
    
    return data_dataframe