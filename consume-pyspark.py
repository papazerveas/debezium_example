from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, from_json
# from pyspark.sql.types import StructType, StructField, StringType

# 1. Start Spark session
spark = (SparkSession.builder
    .appName("DebeziumKafkaConsumer")
    .master("local[*]") 
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.6")
    .config("spark.hadoop.io.native.lib.available", "false")
    .getOrCreate()
)

# 2. Read from Kafka topic
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:29092") \
    .option("subscribe", "local_mysql57.emailtrack_spring.login") \
    .option("startingOffsets", "earliest") \
    .load()


# 3. Get the raw JSON payload as string
json_df = raw_df.selectExpr("*", "CAST(value AS STRING) as json_str").drop("value")


# # 4. Define schema for the outer Debezium payload
# outer_schema = StructType().add("payload", StructType().add("after", StructType([
#     StructField("id", StringType()),
#     StructField("payload", StringType()),
#     StructField("created_at", StringType())
# ])))

# # 5. Parse JSON
# parsed_df = json_df.select(from_json(col("json_str"), outer_schema).alias("data"))

console_query = json_df.writeStream \
    .format("console") \
    .trigger(processingTime='2 seconds') \
    .option("truncate", "false") \
    .start()

parquet_query = json_df.writeStream \
    .format("parquet") \
    .option("path", "./data/spring_login") \
    .option("checkpointLocation", "./checkpoint/spring_login") \
    .trigger(processingTime='2 seconds') \
    .outputMode("append") \
    .start()

console_query .awaitTermination()
parquet_query.awaitTermination()
 
