
## sprint4-support-vector-team
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
  POST /api/data
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `api_key` | `string` | **Obrigatório**. A chave da sua API |



#### Formato dos dados a serem enviados 

`{"PESSOA_PIPEDRIVE_notes_count":1,"PESSOA_PIPEDRIVE_done_activities_count":10,"FUNIL_ONBOARDING_PIPEDRIVE_activities_count":0,"ATENDIMENTOS_AGENDA_Faltas Todos Atendimento":0,"ATENDIMENTOS_AGENDA_Qde Atendimento M\\u00e9dico":1,"ATENDIMENTOS_AGENDA_Faltas Atendimento M\\u00e9dico":0,"ATENDIMENTOS_AGENDA_Qde Atendimentos Acolhimento":2,"ATENDIMENTOS_AGENDA_Faltas Acolhimento":0,"ATENDIMENTOS_AGENDA_Qde Psicoterapia":1,"ATENDIMENTOS_AGENDA_Qde Prescri\\u00e7\\u00f5es":0.0,"TWILIO_Mensagens Inbound":62,"TWILIO_Mensagens Outbound":102,"TWILIO_Liga\\u00e7\\u00f5es Outbound":0,"PESSOA_PIPEDRIVE_age":26,"PESSOA_PIPEDRIVE_has_public_health_plan":1,"PESSOA_PIPEDRIVE_tem_data_dataframe_de_termino_de_contrato":1,"PESSOA_PIPEDRIVE_Tem_Canal_de_Prefer\\u00eancia":0,"PESSOA_PIPEDRIVE_has_notes":1,"WHOQOL_F\\u00edsico_New":-0.5370417547,"WHOQOL_Psicol\\u00f3gico_New":-0.6617507976,"WHOQOL_Social_New":0.4268099387,"WHOQOL_Ambiental_New":5.0,"COMUNICARE_Problemas Abertos Bool":1,"TWILIO_Data \\u00daltima Mensagens Inbound Recente":0,"stay_time":348.0,"TWILIO_Data \\u00daltima Mensagens Outbound Recente":0,"TWILIO_Data \\u00daltima Liga\\u00e7\\u00f5es Outbound Recente":0,"TWILIO_Mensagens J\\u00e1 Enviou":true,"TWILIO_Mensagens Raz\\u00e3o":1.6451612903,"PESSOA_PIPEDRIVE CRIAN\\u00c7A":0,"PESSOA_PIPEDRIVE JOVEM":1,"PESSOA_PIPEDRIVE ADULTO":0,"PESSOA_PIPEDRIVE IDOSO":0,"TWILIO_Liga\\u00e7\\u00f5es Outbound Qtd Significativa":0,"ATENDIMENTOS_AGENDA_Qde Psicoterapia Nenhum":0,"ATENDIMENTOS_AGENDA_Qde Psicoterapia Pouco":1,"ATENDIMENTOS_AGENDA_Qde Psicoterapia Muito":0,"PESSOA_PIPEDRIVE_id_gender Bin\\u00e1rio":1,"FUNIL_ASSINATURA_PIPEDRIVE_id_stage Bin\\u00e1rio":0,"Status_80":true,"Status_81":false,"Status_82":false,"Status_83":false,"Estado_Alagoas":false,"Estado_Amazonas":false,"Estado_Bahia":false,"Estado_Cear\\u00e1":false,"Estado_Distrito Federal":false,"Estado_Esp\\u00edrito Santo":false,"Estado_Maranh\\u00e3o":false,"Estado_Mato Grosso do Sul":false,"Estado_Minas Gerais":false,"Estado_Paran\\u00e1":false,"Estado_Para\\u00edba":false,"Estado_Par\\u00e1":false,"Estado_Pernambuco":false,"Estado_Piau\\u00ed":false,"Estado_Rio Grande do Norte":false,"Estado_Rio Grande do Sul":false,"Estado_Rio de Janeiro":false,"Estado_Santa Catarina":false,"Estado_Sergipe":false,"Estado_State of Amazonas":false,"Estado_S\\u00e3o Paulo":true,"PESSOA_PIPEDRIVE_city Codificada":99,"status_lost":true,"status_won":false,"lost_reason_Outro":false,"lost_reason_[Assinatura] Cancelamento por inadimpl\\u00eancia":false,"lost_reason_[Assinatura] Desligamento":true,"lost_reason_[Assinatura] Empresa cancelou o benef\\u00edcio da Ana":false,"lost_reason_[Assinatura] Est\\u00e1 sem tempo para conciliar os atendimentos":false,"lost_reason_[Assinatura] N\\u00e3o quer seguir com a Ana":false,"lost_reason_[Assinatura] Precisou cortar custos":false,"canal_preferencia_0":true,"canal_preferencia_238":false,"canal_preferencia_239":false,"canal_preferencia_360":false,"Status_N\\u00e3o iniciado":false,"Status_lost":false,"Status_open":false,"Status_won":true,"lost_reason_Outro.1":true,"lost_reason_[Associade] Cancelou assinatura":false,"lost_reason_[Onboarding] N\\u00e3o retornou aos contatos de resgate":false,"lost_reason_[Onboarding] N\\u00e3o tem interesse em seguir nas etapas do onboarding":false,"stage_Boas-vindas":false,"stage_N\\u00e3o iniciado":false,"stage_Primeira reuni\\u00e3o":false,"stage_Question\\u00e1rio":true}`


## Autores

- [@st4pzz](https://github.com/st4pzz)
- [@juliapaiva1](https://github.com/juliapaiva1)
- [@alessitomas](https://github.com/alessitomas)
- [@WeeeverAlex](https://github.com/WeeeverAlex)


