from pyspark.sql import SparkSession

# Start Spark session
spark = (SparkSession.builder
         .appName("DebeziumKafkaConsumer")
         .master("local[*]") 
         .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.6")
         .config("spark.hadoop.io.native.lib.available", "false")
         .getOrCreate()
         )


def enable_stream(session: SparkSession, topic: str = "local_mysql57.apifon_callbacks.test_client"):
    safe_topic = topic.replace("/", "_").replace(".", "_")

    # Read from Kafka topic
    raw_df = (session.readStream
              .format("kafka")
              .option("kafka.bootstrap.servers", "localhost:29092")
              .option("subscribe", topic)
              .option("startingOffsets", "earliest")
              .option("maxOffsetsPerTrigger", 500000)  # set batch size in records
              .load()
              )

    def write_parquet_batch(batch_df, batch_id):
        print(f">>> Batch {batch_id}, count = {batch_df.count()}")
        # You can add transformations here if needed
        batch_df.write.mode("append").parquet(f"./data/{safe_topic}")

    # Get the raw JSON payload as string
    json_df = raw_df.selectExpr("*", "CAST(value AS STRING) as json_str").drop("value")

    # Start query using foreachBatch
    query = (json_df.writeStream
             .foreachBatch(write_parquet_batch)
             .option("checkpointLocation", f"./checkpoint/{safe_topic}")
             .trigger(processingTime='1 seconds')
             .start()
             )
    return query


enable_stream(session=spark, topic="local_mysql57.apifon_callbacks.test_client").awaitTermination()

# spark.stop()

# console_query = json_df.writeStream \
#     .format("console") \
#     .trigger(processingTime='2 seconds') \
#     .option("truncate", "false") \
#     .start()

# parquet_query = json_df.writeStream \
#     .format("parquet") \
#     .option("path", "./data/spring_login") \
#     .option("checkpointLocation", "./checkpoint/spring_login") \
#     .trigger(processingTime='2 seconds') \
#     .outputMode("append") \
#     .start()

# # console_query .awaitTermination()
# parquet_query.awaitTermination()
 
