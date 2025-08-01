from pyspark.sql import SparkSession
from pyspark.sql.functions import get_json_object, col

spark = SparkSession.builder \
    .appName("ReadParquet") \
    .getOrCreate()

# Read the Parquet files
df = spark.read.parquet("data/local_mysql57_apifon_callbacks_test_client")
df.count()
df.select("json_str").show(n=1, truncate=False)



payload_only_df = df.select(
    get_json_object(col("json_str"), "$.payload.after.payload").alias("payload")
)
payload_only_df.show(n=2, truncate=False)

# Show a sample
# print(df.toPandas().head())