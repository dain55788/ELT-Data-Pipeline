# ELT-Data-Pipeline 🚀
## ELT Data Pipeline Project implementation in Data Warehousing environment using DBT, Airflow, PostgreSQL and more!! ⚡
---
## 📕 What is covered in this project?
+ <b>Data Orchestration</b>: Apache Airflow
+ <b>Data Warehousing</b>: PostgreSQL
+ <b>Data Governance and Data Quality (Staging Area)</b>: Great Expectations
+ <b>Data Transformaton and Data Modeling (Star Schema)</b>: DBT (Data Build Tool) 🌟
+ <b>Data Visualization</b>: PowerBI 📊
+ <b>ELT Data Processing Terminology Implemention</b>

## ⛅ API Data Source
In this project, we will take a look at OpenAQ API, read the document here: https://openaq.org/.
Specifically, we will explore the location measurement of air quality of different locations/ countries in the world.
Take a look on how to create your API Key: https://docs.openaq.org/using-the-api/quick-start 

## 🛠️ System Architecture
![SystemArchitecture](https://github.com/user-attachments/assets/7c4c4893-d12a-412c-8002-d769aa54ae99)

## 📁 Repository Structure
```shell
ELT-Data-Pipeline/
├── .env      /* Environment variables */
├── .git/
├── .gitignore
├── .idea/
├── Dockerfile
├── LICENSE
├── Note.txt
├── README.md
├── airflow/      /* Airflow configuration and DAGs */
│   ├── README.md
│   ├── dags/
│   │   ├── __pycache__/
│   │   ├── .gitkeep
│   │   ├── airquality_pipeline_dag.py
│   │   ├── data_migration_dag.py
│   │   └── utils/
│   │       ├── __pycache__/
│   │       ├── airquality_collector.py
│   │       └── migrate_data.py
│   ├── logs/
│   └── plugins/
├── airflow-docker-compose.yaml
├── data/      /* Sample or test data */
│   ├── location_air_quality.json
│   └── sensor_air_quality.json
├── data_validation/      /* Data quality check with Great Expectations */
│   ├── .gitkeep
│   ├── README.md
│   ├── gx/
│   │   ├── .gitignore
│   │   ├── checkpoints/
│   │   ├── expectations/
│   │   ├── great_expectations.yml
│   │   ├── plugins/
│   │   ├── uncommitted/
│   │   └── validation_definitions/
│   └── openaq_data_quality.ipynb
├── dbt_openaq/      /* dbt project for transformations and modeling */
│   ├── .gitignore
│   ├── .user.yml
│   ├── README.md
│   ├── analyses/
│   ├── dbt_packages/
│   ├── dbt_project.yml
│   ├── logs/
│   ├── macros/
│   ├── models/
│   │   └── production/
│   │       ├── dim_date.sql
│   │       ├── dim_instrument.sql
│   │       ├── dim_location.sql
│   │       ├── dim_owner.sql
│   │       ├── dim_parameter.sql
│   │       ├── dim_provider.sql
│   │       ├── dim_sensor.sql
│   │       ├── dim_time.sql
│   │       ├── fact_air_quality_measurement.sql
│   │       └── schema.yml
│   ├── package-lock.yml
│   ├── packages.yml
│   ├── profiles.yml
│   ├── seeds/
│   ├── snapshots/
│   ├── target/
│   └── tests/
├── images/
├── logs/
├── requirements.txt       /* Python dependencies */
├── scripts/          /* Postgres utility scripts */
│   ├── __init__.py
│   ├── __pycache__/
│   ├── create_schema.py
│   ├── create_table.py
│   └── postgresql_client.py
├── test.py
└── venv/

```

## ⚙ Workflow Diagram
![WorkflowDiagram](https://github.com/user-attachments/assets/b3682736-6543-496f-a7c2-7216af31fc0f)
