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

 
docker run --rm -v "$(pwd)":/app -w /app docker.io/bitnami/spark:3.5.6-debian-12-r0 spark-submit /app/consume-pyspark.py
```


## dremio

```bash
docker exec -u 0 -it dremio bash
cp /opt/dremio/data/rzLocalCA.crt /usr/local/share/ca-certificates
update-ca-certificates

curl https://minio4.retailzoom.local
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