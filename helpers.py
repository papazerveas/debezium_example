from pyspark.sql import SparkSession

def enable_stream(
    session: SparkSession,
    kafka_servers = "localhost:29092",
    topic: str = "local_mysql57.apifon_callbacks.test_client"
):
    safe_topic = topic.replace("/", "_").replace(".", "_")

    # Read from Kafka topic
    raw_df = (session.readStream
              .format("kafka")
              .option("kafka.bootstrap.servers", kafka_servers)
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
             .queryName(f"stream_{safe_topic}")
             .foreachBatch(write_parquet_batch)
             .option("checkpointLocation", f"./checkpoint/{safe_topic}")
             .trigger(processingTime='1 seconds')
             .start()
             )
    return query

