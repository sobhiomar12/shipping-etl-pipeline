from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, datediff, to_date

def process_with_spark():
    os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-17-openjdk-amd64'
    
    spark = SparkSession.builder \
        .appName("Shipping_ETL_HDFS") \
        .config("spark.master", "local[*]") \
        .getOrCreate()
    
    # Read from local CSV (inside container)
    orders = spark.read.option("header", "true").csv("/opt/airflow/data/raw/olist_orders_dataset.csv")
    items = spark.read.option("header", "true").csv("/opt/airflow/data/raw/olist_order_items_dataset.csv")
    customers = spark.read.option("header", "true").csv("/opt/airflow/data/raw/olist_customers_dataset.csv")
    sellers = spark.read.option("header", "true").csv("/opt/airflow/data/raw/olist_sellers_dataset.csv")
    
    print(f"Orders: {orders.count()}, Items: {items.count()}")
    
    items = items.withColumn("freight_value", col("freight_value").cast("double"))
    
    fact = orders.join(items, "order_id", "inner") \
                 .join(customers, "customer_id", "left") \
                 .join(sellers, "seller_id", "left") \
                 .filter(col("order_status") == "delivered")
    
    fact = fact.withColumn("shipping_days", 
                          datediff(to_date("order_delivered_customer_date"), 
                                  to_date("order_delivered_carrier_date")))
    
    # Save to HDFS (full path with hdfs://)
    fact.write.mode("overwrite").parquet("hdfs://namenode:9000/user/airflow/fact_shipping")
    
    print(f"✅ Saved to HDFS: {fact.count()} records")
    spark.stop()

default_args = {'owner': 'airflow', 'start_date': datetime(2024,1,1), 'retries': 1}

with DAG('shipping_spark_hdfs_dag', default_args=default_args, schedule_interval='*/15 * * * *', catchup=False) as dag:
    task = PythonOperator(task_id='process_with_spark', python_callable=process_with_spark)