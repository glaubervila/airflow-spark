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
spark_scripts_path = base_path.joinpath("include/spark")

# Datalake path
data_path = base_path.joinpath("data")
# Bronze data path
bronze_path = data_path.joinpath("bronze/twitter_datascience")
# Silver data path
silver_path = data_path.joinpath("silver/twitter_datascience")
# Gold data path
gold_path = data_path.joinpath("gold/twitter_datascience")

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"
query = "datascience"
end_time = datetime.now().strftime(TIMESTAMP_FORMAT)
start_time = (datetime.now() + timedelta(-1)).date().strftime(TIMESTAMP_FORMAT)

with DAG(dag_id="TwitterDAG", start_date=pendulum.datetime(2024, 3, 23, tz="UTC"), schedule_interval="@daily") as dag:

    PARTITION_FOLDER_EXTRACT = f"extract_date={datetime.now().date()}"

    # NEED Connection
    # Type: HTTP
    # ID: twitter_default
    # Host: https://labdados.com
    twitter_operator = TwitterOperator(
        task_id="twitter_datascience",
        file_path=bronze_path.joinpath(
            PARTITION_FOLDER_EXTRACT, f"datascience_{datetime.now().date().strftime('%Y%m%d')}.json"
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
            str(bronze_path),
            "--dest",
            str(silver_path),
            "--process-date",
            "{{ ds }}",
        ],
    )

    twitter_insight = SparkSubmitOperator(
        task_id="insight_twitter",
        application=str(spark_scripts_path.joinpath("insight_tweet.py")),
        name="insight_twitter",
        application_args=[
            "--src",
            str(silver_path),
            "--dest",
            str(gold_path),
            "--process-date",
            "{{ ds }}",
        ],
    )

    twitter_operator >> twitter_transform >> twitter_insight
