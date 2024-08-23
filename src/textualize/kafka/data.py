from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split

spark = SparkSession.builder \
    .appName("ChatAnalysis") \
    .getOrCreate()

# Kafka에서 실시간으로 데이터를 읽어옵니다.
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "chat") \
    .load()

# Kafka 메시지에서 채팅 메시지를 추출합니다.
messages_df = df.selectExpr("CAST(value AS STRING)")

# 메시지에서 주제를 추출하고 분석합니다.
# 예시: 메시지에서 주제 추출
topics_df = messages_df \
    .withColumn("topic", split(col("value"), " ")[0]) \
    .groupBy("topic") \
    .count()

# 결과를 콘솔에 출력하거나 데이터베이스에 저장합니다.
query = topics_df.writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()

