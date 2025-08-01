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
