from airflow.models import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator

from datetime import datetime, timedelta
from pandas import json_normalize
import json

default_args = {
    "owner": "airflow",
    "start_date": datetime(2021, 1, 1),
	#‘end_date’: datetime(2021, 12 , 30),
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

def _processing_user(ti):
    users = ti.xcom_pull(task_ids=['extracting_user'])
    if not len(users) or "results" not in users[0]:
        raise ValueError("User is empty")
    user = users[0]["results"][0]
    processed_user = json_normalize({
        "firstname": user["name"]["first"],
        "lastname": user["name"]["last"],
        "country": user["location"]["country"],
        "username": user["login"]["username"],
        "password": user["login"]["password"],
        "email": user["email"]
    })
    processed_user.to_csv('/tmp/processed_user.csv', index=None, header=False)

with DAG("user_processing", 
        description="Get a random user from an API and save it as CSV",
        schedule_interval="@daily", 
        default_args=default_args, 
        catchup=False) as dag:
        
    is_api_available = HttpSensor(
        task_id="is_api_available",
        http_conn_id="user_api",
        endpoint="api/"
    )

    extracting_user = SimpleHttpOperator(
        task_id="extracting_user",
        http_conn_id="user_api",
        endpoint="api/",
        method="GET",
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    processing_user = PythonOperator(
        task_id="processing_user",
        python_callable=_processing_user
    )

    send_email_notification = EmailOperator(
        task_id="send_email_notification",
        to="hansel@dsaid.gov.sg",
        subject="Pipeline Done User Processed",
        html_content="<h1>Done! Your User Processing Pipeline run has completed!</h1>"
    )

    is_api_available >> extracting_user >> processing_user >> send_email_notification