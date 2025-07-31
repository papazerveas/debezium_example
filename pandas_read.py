import pandas as pd

pdf = pd.read_parquet("./emailtrack_spring_login", engine="pyarrow")
print(pdf.head(n=100 ))

pdf.count()

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ReadParquet") \
    .getOrCreate()

# Read the Parquet files
df = spark.read.parquet("emailtrack_spring_login")
df.count()
# Show a sample
print(df.toPandas().head())