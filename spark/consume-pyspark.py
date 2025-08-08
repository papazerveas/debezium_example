from pyspark.sql import SparkSession
from helpers import enable_stream

# Start Spark session
spark = (SparkSession.builder
         .appName("DebeziumKafkaConsumer")
         .master("local[*]")
         .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.6")
         .config("spark.hadoop.io.native.lib.available", "false")
         .getOrCreate()
         )


q1 = enable_stream(
    session=spark,
    kafka_servers="kafka:9092",
    topic="local_mysql57.apifon_callbacks.test_client",
    output_table="nessie.mysql.beautyline"
)

q2 = enable_stream(
    session=spark,
    kafka_servers="kafka:9092",
    topic="apifon_callback_postgres.public.test_client",
    output_table="nessie.postgres.beautyline"
)

# q1.awaitTermination()
# q2.awaitTermination()

for q in spark.streams.active:
    print(f" ========== ID: {q.id}, Name: {q.name} Active: {q.isActive}, Status: {q.status['message']} {len(q.recentProgress)}")
    # for p in q.recentProgress:
    #     print(p)

    
# Wait for any to terminate (non-blocking for setup)
spark.streams.awaitAnyTermination()

