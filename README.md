
## Sprint4-support-vector-team
`Nosso modelo preditivo é capaz de, através de uma robusta tabela de dados fornecida pela empresa Ana Health, estimar o número de horas que o usuário ficará na plataforma desde a data em que ele entrou, com a finalidade de auxiliar a empresa na redução do churn.`


## Stack utilizada


**Dashboard:** Streamlit

**Banco de Dados:** MongoDB

**Back-end:** Pandas, Matplotlib , missingno, pymongo, bcrypt, plotly, scikit learn, python-dotenv, Flask


## Instalação das Dependencias

Crie um ambiente virtual

```bash
  python3 -m venv env
  source env/bin/activate
```

Instale as Dependencias 

```bash
  pip install -r requirements.txt
```
    
## O conjunto de Dados utilizado foi fornecido pela empresa Ana Health

 - [Tabela de Dados](https://docs.google.com/spreadsheets/d/1ku3RbAe_BQFqSxfEgbJARmUMaKEidGqvWo-xh-E7XE0/edit#gid=841451143)

## Pré-processamento  e Feature Engineering dos Dados

O pré-processamento foi realizado nos notebooks contidos
na pasta 'pré-processamento' dentro da pasta 'notebooks', com o objetivo específico de lidar
com valores nulos. Neste sentido, adotamos estratégias como descartar colunas com
muitos valores nulos, consideradas irrelevantes para o modelo, ou preencher esses valores
nulos com o número 0. Também fizemos feature engineering dos dados, onde criamos novas colunas, 
descartamos outras, entre outros procedimentos. Os notebooks relativos à essas atividades estão na 
pasta "feature engineering". As tabelas criadas pelos processos de pré-processamento e feature engineering se 
encontram na pasta "data".

**A documentação completa sobre todas as manipulações de dados se encontra no arquivo Documentação-Manipulação-de-dados, dentro da pasta doc**

## O modelo

O notebook de treinamento do modelo está contido na pasta `notebooks/modelo_tempo_permanencia.ipynb` , nele foram treinados os algoritmos de `Regressor Linear`, `Random Forest` e `Support Vector Regressor`, juntamente com ajuste de hiperparâmetros com `GridSearch` da biblioteca `scikit-learn`, os resultados obtidos foram

- **Random Forest Regressor**: 
- RMSE: 96.99
- R2: 0.25312721913815717
 - EVS: 0.32890013577762933 
- Erro percentual médio: 15.93% 

- **Support Vector Regressor**: 
- RMSE: 85.63
- R2: 0.4178046750004776 
- EVS: 0.43484915131508506
- Erro percentual médio: 14.06% 

- **Linear Regression**:
- RMSE: 167.07
- R2: -1.2161651340448807
- EVS: -1.1666649285715551 
- Erro percentual médio: 27.43% 

`Utilizamos métricas como RMSE, R2, EVS e o erro percentual médio para avaliação.
RMSE significa “erro quadrático médio”, R2 é o coeficiente de determinação e EVS significa
“explained variance score”.`

Tivemos o melhor desempenho com o algoritmo Support Vector Regressor, com os hiperparâmetros: 
'poly_features__degree': 1, 
'svr__C': 1, 
'svr__epsilon': 0.1, 
'svr__kernel': 'linear'

## Resultados obtidos

Por ter sido treinado em um conjunto de dados com pouco tempo, e com pessoas que saíram da empresa, não é ideal utilizá-lo para prever o tempo restante de pessoas que ainda estão na plataforma. Entretanto, é possível utilizá-lo para ver se uma pessoa ficou mais ou menos tempo do que o previsto, e a partir disso, identificar possíveis razões pelas quais a pessoa saiu da plataforma antes do esperado.

## Documentação da API

#### Retorna o tempo estimado, em dias, de permanência do usuario na plataforma.

```http
  POST http://54.191.142.192:8082/predict
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `X_API_KEY` | `string` | **Obrigatório**. A chave da sua API |



#### Formato dos dados a serem enviados 

`{"PESSOA_PIPEDRIVE_id_person":"1260","PESSOA_PIPEDRIVE_birthdate":"1995-04-05","PESSOA_PIPEDRIVE_id_gender":"63","PESSOA_PIPEDRIVE_id_marrital_status":"80","PESSOA_PIPEDRIVE_state":"São Paulo","PESSOA_PIPEDRIVE_city":"São Carlos","PESSOA_PIPEDRIVE_postal_code":"13560-470","PESSOA_PIPEDRIVE_id_health_plan":"412","PESSOA_PIPEDRIVE_id_person_recommendation":null,"PESSOA_PIPEDRIVE_contract_start_date":"2021-08-12","PESSOA_PIPEDRIVE_contract_end_date":"2022-09-11","PESSOA_PIPEDRIVE_id_continuity_pf":"339","PESSOA_PIPEDRIVE_Canal de Preferência":null,"PESSOA_PIPEDRIVE_notes_count":"1","PESSOA_PIPEDRIVE_done_activities_count":"3","PESSOA_PIPEDRIVE_Recebe Comunicados?":null,"PESSOA_PIPEDRIVE_Interesses":null,"PESSOA_PIPEDRIVE_Pontos de Atenção":null,"FUNIL_ASSINATURA_PIPEDRIVE_id_stage":"65","FUNIL_ASSINATURA_PIPEDRIVE_id_org":"448","FUNIL_ASSINATURA_PIPEDRIVE_status":"lost","FUNIL_ASSINATURA_PIPEDRIVE_start_of_service":"2021-08-12","FUNIL_ASSINATURA_PIPEDRIVE_lost_time":"2022-09-11 03:00:00","FUNIL_ASSINATURA_PIPEDRIVE_lost_reason":"[Assinatura] Desligamento","FUNIL_ONBOARDING_PIPEDRIVE_add_time":"2021-09-09 13:44:13","FUNIL_ONBOARDING_PIPEDRIVE_status":"open","FUNIL_ONBOARDING_PIPEDRIVE_id_label":"325","FUNIL_ONBOARDING_PIPEDRIVE_stay_in_pipeline_stages_welcome":"0","FUNIL_ONBOARDING_PIPEDRIVE_stay_in_pipeline_stages_first_meeting":"0","FUNIL_ONBOARDING_PIPEDRIVE_stay_in_pipeline_stages_whoqol":"29770","FUNIL_ONBOARDING_PIPEDRIVE_won_time":null,"FUNIL_ONBOARDING_PIPEDRIVE_lost_time":null,"FUNIL_ONBOARDING_PIPEDRIVE_lost_reason":null,"FUNIL_ONBOARDING_PIPEDRIVE_activities_count":"0","ATENDIMENTOS_AGENDA_Qde Todos Atendimentos":"0","ATENDIMENTOS_AGENDA_Faltas Todos Atendimento":"0","ATENDIMENTOS_AGENDA_Qde Atendimento Médico":null,"ATENDIMENTOS_AGENDA_Faltas Atendimento Médico":null,"ATENDIMENTOS_AGENDA_Datas Atendimento Médico":null,"ATENDIMENTOS_AGENDA_Qde Atendimentos Acolhimento":null,"ATENDIMENTOS_AGENDA_Faltas Acolhimento":null,"ATENDIMENTOS_AGENDA_Datas Acolhimento":null,"ATENDIMENTOS_AGENDA_Qde Psicoterapia":null,"ATENDIMENTOS_AGENDA_Faltas Psicoterapia":null,"ATENDIMENTOS_AGENDA_Datas Psicoterapia":null,"ATENDIMENTOS_AGENDA_Qde Prescrições":"1","ATENDIMENTOS_AGENDA_Datas Prescrição":"07\\/12\\/2021","WHOQOL_Qde Respostas WHOQOL":"1","WHOQOL_Físico":"4,00","WHOQOL_Psicológico":"4","WHOQOL_Social":"4","WHOQOL_Ambiental":"5","COMUNICARE_Problemas Abertos":"diabetes de tipo 2 T90 (CIAP-2); ansiedade P01 (CIAP-2); obesidade com imc>=30 T82 (CIAP-2); carência de vitamina D T91 (CIAP-2); saliva anormal A91 (CIAP-2)","TWILIO_Mensagens Inbound":"74","TWILIO_Data Última Mensagens Inbound":"2022-06-22 06:20:09","TWILIO_Mensagens Outbound":"53","TWILIO_Data Última Mensagens Outbound":"2022-08-23 11:36:44","TWILIO_Ligações Inbound":null,"TWILIO_Data Última Ligações Inbound":null,"TWILIO_Ligações Outbound":null,"TWILIO_Data Última Ligações Outbound":null,"COBRANÇA_VINDI_Qde Total de Faturas":null,"COBRANÇA_VINDI_Qde Total de Tentativas de Cobrança":null,"COBRANÇA_VINDI_Método de Pagamento":null,"COBRANÇA_VINDI_Valor Médio da Mensalidade":null,"COBRANÇA_VINDI_Qde Total de Faturas Pagas após Vencimento":null,"COBRANÇA_VINDI_Qde Total de Faturas Inadimpletes":null,"COBRANÇA_VINDI_Valor Total Inadimplência":null,"COBRANÇA_VINDI_Qde Perfis de Pagamento Inativos":null}`


## Autores

- [@st4pzz](https://github.com/st4pzz)
- [@juliapaiva1](https://github.com/juliapaiva1)
- [@alessitomas](https://github.com/alessitomas)
- [@WeeeverAlex](https://github.com/WeeeverAlex)


