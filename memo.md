## Install TimeScaleDB extension 

- Connect with psql on your database with your credentials. 
- Create a database, go on this database and install the extension

```sql 
CREATE database tsdb;
\c tsdb
CREATE EXTENSION IF NOT EXISTS timescaledb;
\dx 
```

## Create Hypertable 

- 