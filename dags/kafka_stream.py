from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import logging

default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2023, 9, 3, 10, 0),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

def get_data():
    import requests
    res = requests.get("https://randomuser.me/api/").json()
    return res['results'][0]

def format_data(res):
    location = res['location']
    return {
        'first_name': res['name']['first'],
        'last_name': res['name']['last'],
        'gender': res['gender'],
        'address': f"{location['street']['number']} {location['street']['name']}, "
                   f"{location['city']}, {location['state']}, {location['country']}",
        'postcode': location['postcode'],
        'email': res['email'],
        'username': res['login']['username'],
        'dob': res['dob']['date'],
        'registered_date': res['registered']['date'],
        'phone': res['phone'],
        'picture': res['picture']['medium']
    }

def stream_data():
    import json, time
    from kafka import KafkaProducer
    import kafka

    logging.info(f"Kafka module loaded from: {kafka.__file__}")

    try:
        producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
        logging.info("Connected to Kafka successfully")
    except Exception as e:
        logging.error(f"Could not connect to Kafka: {e}")
        raise

    curr_time = time.time()
    while time.time() - curr_time < 60:
        try:
            res = get_data()
            res = format_data(res)
            producer.send('users_created', json.dumps(res).encode('utf-8'))
            producer.flush()
            logging.info("Message sent successfully")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            continue

with DAG(
    'user_automation',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:
    streaming_task = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data,
        execution_timeout=timedelta(minutes=2)
    )


