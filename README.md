\curl http://localhost:8083/connector-plugins


## MySqlConnector

```
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

## spark

```bash
conda create -n spark python==3.12.3
conda activate spark
pip install -r requirenents.txt
```
