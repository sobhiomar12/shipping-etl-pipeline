from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import os

def process_shipping_data():
    data_dir = '/opt/airflow/data/raw'
    output_dir = '/opt/airflow/data/processed'
    
    print("📂 Loading data...")
    
    orders = pd.read_csv(os.path.join(data_dir, 'olist_orders_dataset.csv'))
    items = pd.read_csv(os.path.join(data_dir, 'olist_order_items_dataset.csv'))
    customers = pd.read_csv(os.path.join(data_dir, 'olist_customers_dataset.csv'))
    sellers = pd.read_csv(os.path.join(data_dir, 'olist_sellers_dataset.csv'))
    
    print(f"✅ Orders: {len(orders)}, Items: {len(items)}")
    
    # Merge to create fact table
    fact = orders.merge(items, on='order_id') \
                 .merge(customers, on='customer_id', how='left') \
                 .merge(sellers, on='seller_id', how='left')
    
    fact = fact[fact['order_status'] == 'delivered']
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Save fact table
    fact.to_parquet(os.path.join(output_dir, 'fact_shipping.parquet'), index=False)
    
    # Save dimensions
    customers.drop_duplicates().to_parquet(os.path.join(output_dir, 'dim_customer.parquet'), index=False)
    sellers.drop_duplicates().to_parquet(os.path.join(output_dir, 'dim_seller.parquet'), index=False)
    
    print(f"🎯 Fact table: {len(fact)} records")
    print(f"🎯 Dim Customer: {len(customers)}")
    print(f"🎯 Dim Seller: {len(sellers)}")
    print("✅ Data saved to /opt/airflow/data/processed/")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    'shipping_etl_dag',
    default_args=default_args,
    schedule_interval='*/15 * * * *',
    catchup=False,
    description='ETL for Shipping Analytics',
) as dag:
    
    process_task = PythonOperator(
        task_id='process_shipping_data',
        python_callable=process_shipping_data,
    )