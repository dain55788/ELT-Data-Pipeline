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
  │
  ├── airflow/                     # Airflow setup
  │   ├── dags/                    # Airflow DAG definitions
  │   │   ├── utils/               # Helper functions for DAGs
  │   │   │   ├── airquality_collector.py  # Data collection functions
  │   │   │   └── migrate_data.py          # Data migration functions
  │   │   ├── airquality_pipeline_dag.py   # DAG for data extraction
  │   │   └── data_migration_dag.py        # DAG for data loading
  │   ├── logs/                    # Airflow logs
  │   └── plugins/                 # Airflow plugins
  │
  ├── data/                        # Data storage
  │   ├── location_air_quality.json  # Extracted location data
  │   └── sensor_air_quality.json    # Extracted sensor data
  │
  ├── data_validation/             # Great Expectations (not yet implemented)
  │
  ├── dbt_openaq/                  # DBT project for transformations
  │   ├── models/                  # DBT transformation models
  │   ├── tests/                   # DBT tests
  │   ├── seeds/                   # Static data for DBT
  │   ├── snapshots/               # DBT snapshots
  │   ├── macros/                  # DBT macros
  │   ├── analyses/                # DBT analyses
  │   ├── dbt_project.yml          # DBT project configuration
  │   └── profiles.yml             # DBT connection profiles
  │
  ├── images/                      # System architecture diagrams
  │
  ├── logs/                        # Application logs
  │
  ├── scripts/                     # Setup and utility scripts
  │   ├── postgresql_client.py     # Database connection utility
  │   ├── create_schema.py         # Schema creation script
  │   └── create_table.py          # Table creation script
  │
  ├── .env                         # Environment variables
  ├── airflow-docker-compose.yaml  # Docker compose for Airflow
  ├── Dockerfile                   # Docker image definition
  ├── requirements.txt             # Python dependencies
  └── README.md                    # Project documentation

```

## ⚙ Workflow Diagram
![WorkflowDiagram](https://github.com/user-attachments/assets/b3682736-6543-496f-a7c2-7216af31fc0f)
