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

- Create a table and then add an hypertable with the name of the tabulations in the table.

```sql 
CREATE TABLE stocks_real_time (
  time TIMESTAMPTZ NOT NULL,
  symbol TEXT NOT NULL,
  price DOUBLE PRECISION NULL,
  day_volume INT NULL
);
SELECT create_hypertable('stocks_real_time','time');
CREATE INDEX ix_symbol_time ON stocks_real_time (symbol, time DESC);
```

- Create a regular postgresql table for relational data with the hypertable. 

```sql
CREATE TABLE company (
  symbol TEXT NOT NULL,
  name TEXT NOT NULL
);
```

## Add time series data to the hypertable

- First download some data and then add it to the hypertable. 

```bash
unzip real_time_stock_data.zip
```

The zip can be found on the tutorial [timescaleDocs](https://docs.timescale.com/getting-started/latest/add-data/).
I put it in a subfolder called `data` and I unziped it in the subfolder. 

```sql
\COPY stocks_real_time from './data/tutorial_sample_tick.csv' DELIMITER ',' CSV HEADER;
\COPY stocks_real_time from './data/tutorial_sample_tick.csv' DELIMITER ',' CSV HEADER;
```

## Look at your data 

- Query your data to get what you want.

```sql 
SELECT * FROM stocks_real_time srt
WHERE time > now() - INTERVAL '4 days';
```



