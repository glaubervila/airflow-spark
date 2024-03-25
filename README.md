# Airflow Devcontainer

<!-- Configurar os lints baseado no repositorio do airflow -->
<!-- https://github.com/apache/airflow/blob/main/.gitignore -->

https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html


Based on these articles

https://medium.com/@paulmartins/debugging-airflow-with-vscode-21dbd41d4de6

https://levelup.gitconnected.com/debugging-airflow-dags-in-containers-with-vs-code-e31c0e899c7e

https://davidgriffiths-data.medium.com/debugging-airflow-in-a-container-with-vs-code-7cc26734444


```bash
gh repo clone glaubervila/airflow_devcontainer
```

```bash
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

```bash
docker compose up airflow-init
```

```bash
docker compose up
```


### Export/Import Connections to Json file

```bash
airflow connections export src/config/connections.json
```

```bash
airflow connections import src/config/connections.json
```

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
