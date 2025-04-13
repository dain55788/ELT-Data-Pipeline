# Data Modeling - Data Transformation DBT

![DBT-Logo](https://github.com/user-attachments/assets/9ffef0a6-8cce-436f-9820-31bdffa7f12d)

## Getting started

1. **Create dbt project**
   
```bash
dbt init
```

Run this command, name the project dbt_openaq and fill some neccessary fields (port, username, password, ...), after that you can see a similar tree folder with the following structure:

```shell
├──dbt_openaq/
    ├── analyses/
    ├── dbt_packages/ /* you can see after running dbt deps /
    ├── logs/
    │     └── dbt.log
    ├── macros/ /* contain functions to use in models /
    ├── models/
    │     └── production/
    │     ├── dim_date.sql
    │     ├── dim_instrument.sql
    │     ├── dim_location.sql
    │     ├── dim_owner.sql
    │     ├── dim_parameter.sql
    │     ├── dim_provider.sql
    │     ├── dim_sensor.sql
    │     ├── dim_time.sql
    │     ├── fact_air_quality_measurement.sql
    │     └── schema.yml
    ├── seeds/ /* contain data file for ingesting into the data warehouse /
    ├── snapshots/ /* snapshots to record changes to mutable table over time (SCD Type 2) /
    ├── target/
    ├── tests/
    ├── .gitignore
    ├── .user.yml
    ├── dbt_project.yml
    ├── package-lock.yml
    ├── packages.yml /* create to install deps /
    ├── profiles.yml
    └── README.md
```

2. **Manage dependencies**:

Create `packages.yml` into `dbt_nyc` folder:

```txt
packages:
  - package: dbt-labs/dbt_utils
    version: 0.8.0
```

Then run this `dbt deps` to install the packages - by default this directory is ignored by git, to avoid duplicating the source code for the package.

```bash
dbt deps
```

3. **Run this command to check your connection to your database, Git**

```bash
dbt debug
```

![Screenshot 2025-04-13 002519](https://github.com/user-attachments/assets/b1f479ce-5052-47be-94a3-f15c21178ab4)

4. **Try running the following commands to implement the transformed models dbt**

```bash
dbt run
```

![Screenshot 2025-04-13 004748](https://github.com/user-attachments/assets/29e3c610-4060-4863-b225-1eb0b561764e)

```bash
dbt test
```

### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices

---
<p>&copy; 2025 NguyenDai</p>
