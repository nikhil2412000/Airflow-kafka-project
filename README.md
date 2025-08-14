# Airflow-kafka-project
# Airflow-Kafka Data Streaming Project

## Overview
This project demonstrates a **real-time data streaming pipeline** using Apache Airflow and Kafka. It fetches random user data from a public API, formats it, and streams it to a Kafka topic. The entire system is containerized using Docker Compose for easy deployment and reproducibility.

---

## Features
- **Airflow DAG** to fetch, transform, and stream data.
- **Kafka** for real-time messaging and data storage.
- **Docker Compose** to orchestrate Airflow, Kafka, Zookeeper, Postgres, and other services.
- Robust **error handling and logging** for API failures and Kafka connectivity issues.
- Demonstrates full **data engineering workflow**: API → Airflow → Kafka → Consumer.

---

## Technologies Used
- Python
- Apache Airflow
- Apache Kafka
- Docker & Docker Compose
- REST API
- Postgres
- Bash scripting

---

## Architecture
1. Airflow DAG triggers `stream_data()` function.
2. Fetches user data from `https://randomuser.me/api/`.
3. Formats the data (name, email, address, etc.).
4. Streams the data to Kafka topic `users_created`.
5. Kafka stores the messages for downstream consumers.


---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/nikhil2412000/airflow-kafka-project.git
cd airflow-kafka-project
