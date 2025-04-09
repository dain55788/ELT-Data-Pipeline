# Airflow - Data Orchestration
![Airflow-Logo](https://github.com/user-attachments/assets/f44c3afe-afaa-4143-9552-be803cb66204)

## Getting started
1. **Create Airflow Project**:
```bash
  docker compose -f airflow-docker-compose.yaml up -d
```

2. **Access the Airflow Webserver UI**
   
   Airflow Webserver UI is accessible at `http://localhost:8080/` and login with username && password is `airflow`

3. **PostgresSQL Connection**

   Prerequisites:
   
![PostgreSQLConnection](https://github.com/user-attachments/assets/88f69401-acef-4dab-9dc8-97e9b939fe9f)

   + On your Airflow Webserver UI, click Admin --> Hit the '+' --> Add new Connection
   + Fill required fields (connection id, connection type, host, port, login, password and schema name are required)
   
4. **Trigger DAG**
   You can manually trigger the DAG to run.

---
<p>&copy; 2025 NguyenDai</p>
