# Pipeline ETL utilizando Apache airflow e spark

Este projeto foi feito para estudo das ferramentas Airflow e Spark, no contexto da Formação Apache Airflow da Alura, mas tem como diferencial o ambiente em containers.

## Sobre

Neste projeto foi implementada uma DAG **TwitterDAG** que é um data pipeline ETL (extract, tranform, load), que consulta uma api que gera dados fakes de twitter, baixa os dados para uma palavra especifica e organiza os resultados da api em diretórios e dataframes cada vez mais refinados.

e o datalake segue o padrão medalha contendo 3 diretórios bronze para dados brutos, prata para os dados tratados e gold para os dados finais refinados.

A Primeira etapa é a de extração que utiliza **TwitterHook** um HttpHook para executar as requisições a api <https://labdados.com> e o **TwitterOperator** que organiza os resultado da api no diretório data/bronze.

Schema Original dos dados Brutos (Bronze) 

```markdown
root
 |-- data: array (nullable = true)
 |    |-- element: struct (containsNull = true)
 |    |    |-- author_id: string (nullable = true)
 |    |    |-- conversation_id: string (nullable = true)
 |    |    |-- created_at: string (nullable = true)
 |    |    |-- edit_history_tweet_ids: array (nullable = true)
 |    |    |    |-- element: long (containsNull = true)
 |    |    |-- id: string (nullable = true)
 |    |    |-- in_reply_to_user_id: string (nullable = true)
 |    |    |-- lang: string (nullable = true)
 |    |    |-- public_metrics: struct (nullable = true)
 |    |    |    |-- like_count: long (nullable = true)
 |    |    |    |-- quote_count: long (nullable = true)
 |    |    |    |-- reply_count: long (nullable = true)
 |    |    |    |-- retweet_count: long (nullable = true)
 |    |    |-- text: string (nullable = true)
 |-- includes: struct (nullable = true)
 |    |-- users: array (nullable = true)
 |    |    |-- element: struct (containsNull = true)
 |    |    |    |-- created_at: string (nullable = true)
 |    |    |    |-- id: string (nullable = true)
 |    |    |    |-- name: string (nullable = true)
 |    |    |    |-- username: string (nullable = true)
 |-- meta: struct (nullable = true)
 |    |-- next_token: string (nullable = true)
 |-- extract_date: date (nullable = true)
```

A Segunda etapa é a de transformação que utiliza o **SparkSubmitOperator** e o script `/src/include/spark/transformation.py` para tratar os dados brutos e organizar em dois spark dataframe (tweets, users) formando assim a camada silver do datalake.

A Terceira etapa seria a de Load, mas neste exemplo está apenas gerando um dataframe com dados sumarizados formando assim a camada gold do nosso datalake. este processamento também é feito utilizando o **SparkSubmitOperator** mas desta vez executando o script `/src/include/spark/insight_tweet.py`

Schema ao final do pipeline (Gold)

```markdown
root
 |-- created_date: date (nullable = true)
 |-- n_tweets: long (nullable = false)
 |-- n_like: long (nullable = true)
 |-- n_quote: long (nullable = true)
 |-- n_reply: long (nullable = true)
 |-- n_retweet: long (nullable = true)
 |-- weekday: string (nullable = true)
```

Dataframe pronto para analise

```markdown
+------------+--------+------+-------+-------+---------+-------+
|created_date|n_tweets|n_like|n_quote|n_reply|n_retweet|weekday|
+------------+--------+------+-------+-------+---------+-------+
|  2024-03-24|       6|   255|    282|    321|      230|    Sun|
|  2024-03-25|       4|   201|    272|    170|      182|    Mon|
+------------+--------+------+-------+-------+---------+-------+
```

## Tecnologias utilizadas

Este projeto conta com:

- Ambiente em containers utilizando docker e docker compose.
- Um devcontainer para usuarios de Vscode.
- Enviroment python 3.8.
- Airflow 2.8.0.
- apache-airflow-providers-apache-spark 4.7.1.
- pyspark 3.3.1.

## Instalação

Git clone e criação dos diretórios.

```bash
gh repo clone glaubervila/airflow-spark
&& mkdir -p airflow-spark/logs airflow-spark/data
&& sudo chown -R 1000:0 airflow-spark
&& chmod -R g+w airflow-spark
&& cd airflow-spark
&& echo -e "AIRFLOW_UID=$(id -u)" > .env
docker compose up airflow-init
```

Import connections

```bash
docker compose run -it --rm airflow-cli airflow connections import /home/airflow/workspaces/airflow-spark/src/config/connections.json
```

## Start/Stop services

Todos os servições podem ser ligados utilizando o comando compose up -d. 
OBS: a interface web está configurada para porta 80. caso necessário edite o docker-compose.yml e altere a porta.

```bash
docker compose up -d
```

Ou acesse a pasta com vscode e ligue o devcontainer.

para desligar os serviços utilize o comando

```bash
docker compose stop
```

### Export/Import Connections to Json file

Estes comandos são uteis para exportar os dados de conexção entre ambientes.

```bash
airflow connections export src/config/connections.json
```

```bash
airflow connections import src/config/connections.json
```
