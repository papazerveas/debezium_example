# Debezium spark connect

## REST Calls

```bash
curl http://localhost:8083/connector-plugins

curl http://localhost:8083/connectors/local_postgres/status | jq

```

## Create a connector

### MySqlConnector

```text
name=local_mysql57

connector.class=io.debezium.connector.mysql.MySqlConnector
database.user=emailtrack
topic.prefix=local_mysql57
schema.history.internal.kafka.topic=dbz-schema-history-mysql
database.server.id=1
tasks.max=1
database.hostname=local_mysql57
database.connectionTimeZone=Europe/Athens
database.password=xxxx
schema.history.internal.kafka.bootstrap.servers=kafka:9092
database.port=3306

# filter database and list
database.include.list=apifon_callbacks
table.include.list=apifon_callbacks.test_client
```

### PostgresConnector

edit postgresql.conf

```text
wal_level = logical
max_replication_slots = 10
max_wal_senders = 10
```

```text
name=local_postgres
connector.class=io.debezium.connector.postgresql.PostgresConnector
tasks.max=1

# PostgreSQL DB connection
database.hostname=apifon_callback_postgres
database.port=5432
database.user=myapp
database.password=secret
database.dbname=apifon_callbacks

# Kafka settings
topic.prefix=apifon_callback_postgres
#schema.history.internal.kafka.bootstrap.servers=kafka:9092
#schema.history.internal.kafka.topic=dbz-schema-history-postgres

# Optional settings
#database.include.list=apifon_callbacks
plugin.name=pgoutput
#slot.name=debezium_slot
#publication.name=debezium_publication


table.include.list=apifon_callback_postgres.public.test_client

```

## spark

```bash
conda create -n spark python==3.12.3
conda activate spark
pip install -r requirenents.txt
```

## spark on docker

```bash
 
docker run --rm -it -v .:/app -v C:/Users/sotiris.p/.ivy2:/opt/bitnami/spark/.ivy2 -w /app --network rz_network bitnami/spark:3.5.6  bash

 
docker run --rm -v .:/app -v C:/Users/sotiris.p/.ivy2:/opt/bitnami/spark/.ivy2 -w /app --network rz_network bitnami/spark:3.5.6 spark-submit /app/consume-pyspark.py
```

## dremio

```bash
docker exec -u 0 -it dremio bash
cp /opt/dremio/data/rzLocalCA.crt /usr/local/share/ca-certificates
update-ca-certificates

curl https://minio4.retailzoom.local:9000
ls /usr/local/share/ca-certificates

keytool -importcert \
  -file /usr/local/share/ca-certificates/rzLocalCA.crt \
  -alias rzLocalCA \
  -keystore /opt/java/openjdk/lib/security/cacerts \
  -storepass changeit \
  -noprompt


fs.s3a.endpoint - minio4.retailzoom.local
fs.s3a.path.style.access - true
dremio.s3.compat   true
```

## nessie

```bash
https://blog.min.io/uncover-data-lake-nessie-dremio-iceberg/

 http://nessie:19120/api/v2
```

```sql
CREATE TABLE SalesData (
    id INT,
    product_name VARCHAR,
    sales_amount DECIMAL,
    transaction_date DATE
) PARTITION BY (transaction_date);

INSERT INTO SalesData (id, product_name, sales_amount, transaction_date)
VALUES
    (1, 'ProductA', 1500.00, '2023-10-15'),
    (2, 'ProductB', 2000.00, '2023-10-15'),
    (3, 'ProductA', 1200.00, '2023-10-16'),
    (4, 'ProductC', 1800.00, '2023-10-16'),
    (5, 'ProductB', 2200.00, '2023-10-17');
```


## hive

```bash
Unable to load AWS credentials from environment variables (AWS_ACCESS_KEY_ID (or AWS_ACCESS_KEY) and AWS_SECRET_KEY (or AWS_SECRET_ACCESS_KEY))


hive doesn't support direct query - try nessie

Connection Properties
----------------------

fs.s3a.path.style.access true
dremio.s3.compat true
fs.s3a.endpoint minio4.retailzoom.local:9000
fs.s3a.access.key 4V3mrry88LHfsZTNCroS
fs.s3a.secret.key VRVqQeOq0I2uLLLHRLRlRFBGfzzh7ZSkpsih55Gh
fs.s3.impl org.apache.hadoop.fs.s3a.S3AFileSystem
fs.s3a.aws.credentials.provider org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider
```
