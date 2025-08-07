
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


## Spark

```bash
docker run --rm -it -v ./spark/cacerts:/opt/bitnami/java/lib/security/cacerts  -v ./spark:/app -v /mnt/Stats/SASDistributed/k3s/pvc-407bac96-4230-4fd7-949a-4832d3817212:/opt/bitnami/spark/.ivy2 -w /app --network rz_network bitnami/spark:3.5.6 bash

# docker run --rm -it  -v ./spark:/app -v /mnt/Stats/SASDistributed/k3s/pvc-407bac96-4230-4fd7-949a-4832d3817212:/root/.ivy2 -w /app --network rz_network hadoop04:5000/spark-delta-aws:3.5.6 bash

 
export SPARK_CONF_DIR=/app 
export AWS_SHARED_CREDENTIALS_FILE=/app/.aws/credentials
export AWS_CONFIG_FILE=/app/.aws/config
export AWS_PROFILE=demo
export SPARK_JARS_IVY=/root/.ivy2
```
 
```python
import os
from pyspark.sql import SparkSession
# Set environment variable to custom config directory
os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "/app"
os.environ["SPARK_CONF_DIR"] = "/app/.aws/credentials"
os.environ["AWS_CONFIG_FILE"] = "/app/.aws/config"
os.environ["AWS_PROFILE"] = "demo"

spark = SparkSession.builder \
    .appName("Spark-Nessie") \
    .getOrCreate()
spark.sql("SHOW TABLES IN nessie").show()

spark.table("nessie.SalesData").show()
 
for k, v in spark.sparkContext.getConf().getAll():
    print(f"{k} = {v}")


# print(spark.sparkContext.getConf().getAll())

spark.sql("SHOW NAMESPACES IN nessie").show()
spark.sql("CREATE NAMESPACE IF NOT EXISTS nessie.sales")

spark.sql("USE nessie.sales")
spark.sql("SHOW TABLES").show()

spark.sql("""
CREATE TABLE SalesData2 (
  id INT,
  product_name STRING,
  sales_amount DECIMAL(10,2),
  transaction_date DATE
)
PARTITIONED BY (transaction_date)
""")

spark.table("nessie.SalesData").show()
```