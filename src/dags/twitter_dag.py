import sys

sys.path.append("/opt/airflow")

from datetime import datetime, timedelta
from pathlib import Path

import pendulum
from airflow.models import DAG
from airflow.operators.empty import EmptyOperator

from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.dates import days_ago

from include.operators.twitter_operator import TwitterOperator

base_path = Path("/opt/airflow")
data_path = base_path.joinpath("data")
spark_scripts_path = base_path.joinpath("include/spark")


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"
query = "datascience"
end_time = datetime.now().strftime(TIMESTAMP_FORMAT)
start_time = (datetime.now() + timedelta(-1)).date().strftime(TIMESTAMP_FORMAT)

with DAG(dag_id="TwitterDAG", start_date=pendulum.datetime(2024, 3, 23, tz="UTC"), schedule_interval="@daily") as dag:

    # Teste celery task
    tarefa_1 = EmptyOperator(task_id="tarefa_1")

    # NEED Connection
    # Type: HTTP
    # ID: twitter_default
    # Host: https://labdados.com
    twitter_operator = TwitterOperator(
        task_id="twitter_datascience",
        file_path=data_path.joinpath(
            f"twitter_datascience/extract_date={datetime.now().date()}/datascience_{datetime.now().date().strftime('%Y%m%d')}.json"
        ),
        query=query,
        start_time=start_time,
        end_time=end_time,
    )

    # NEED Connection
    # Type: Spark
    # ID: spark_default
    # Host: local
    # Deploy Mode: client
    # Spark binary: spark-submit
    twitter_transform = SparkSubmitOperator(
        task_id="transform_twitter_datascience",
        application=str(spark_scripts_path.joinpath("transformation.py")),
        name="twitter_transformation",
        application_args=[
            "--src",
            str(data_path.joinpath("twitter_datascience")),
            "--dest",
            str(data_path.joinpath("silver/twitter_datascience")),
            "--process-date",
            "{{ ds }}",
        ],
    )

    # tarefa_1 >> twitter_operator >> twitter_transform
    tarefa_1 >> twitter_operator >> twitter_transform
