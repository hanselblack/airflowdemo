## Getting Started

- Clone this repo
- Install the prerequisites
- Run the service
- Check http://localhost:8080

### Prerequisites

- Install [Docker](https://www.docker.com/)
- Install [Docker Compose](https://docs.docker.com/compose/install/)
- Following the Airflow release from [Python Package Index](https://pypi.python.org/pypi/apache-airflow)

### Usage

Run the following command to initialize the environment
```
mkdir ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```

On all operating systems, you need to run database migrations and create the first user account. To do it, run.

```
docker-compose up airflow-init
```

Run the web service with docker

```
docker-compose up -d

# Build the image
# docker-compose up -d --build
```

Check http://localhost:8080/

Login with 
- User : airflow
- Password : airflow

## Configure Airflow SMTP

Edit the docker-compose.yml file to set the email provider you are using
Example:
```
AIRFLOW__SMTP__SMTP_HOST: 'smtp.gmail.com'
AIRFLOW__SMTP__SMTP_PORT: '587'
AIRFLOW__SMTP__SMTP_USER: 'xxx@gmail.com'
AIRFLOW__SMTP__SMTP_PASSWORD: 'xxx'
AIRFLOW__SMTP__SMTP_MAIL_FROM: 'xxx@gmail.com'
```

## Other commands

If you want to run airflow sub-commands, you can do so like this:

- `docker-compose run --rm airflow-webserver airflow test [DAG_ID] [TASK_ID] [EXECUTION_DATE]` - Test specific task
- `docker-compose run --rm airflow-webserver airflow tasks test user_processing send_email_notification 2021-01-01`

If you want to run/test python script, you can do so like this:
- `docker-compose run --rm webserver python /usr/local/airflow/dags/[PYTHON-FILE].py` - Test python script

## Connect to database

If you want to use Ad hoc query, make sure you've configured connections:
Go to Admin -> Connections and Edit "postgres_default" set this values:
- Host : postgres
- Schema : airflow
- User : airflow
- Password : airflow
