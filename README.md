# 🚚 Shipping ETL Pipeline

ETL Pipeline for shipping data analysis using **Apache Airflow**, **Apache Spark**, **HDFS**, and **Streamlit**.

## 📌 Project Overview

This project processes Brazilian E-Commerce (Olist) shipping data to:
- Clean and transform raw CSV data
- Create Star Schema (Fact + Dimension tables)
- Store processed data on HDFS
- Visualize insights via interactive dashboard

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Apache Airflow | Workflow orchestration (DAG runs every 15 min) |
| Apache Spark | Data transformation |
| HDFS (Hadoop) | Distributed storage |
| Docker | Containerization |
| Streamlit | Interactive Dashboard |
| Python (Pandas, PySpark) | Data processing |

## 📊 Star Schema

- **Fact Table:** `fact_shipping` (order_id, freight_value, shipping_days)
- **Dimensions:** `dim_customer`, `dim_seller`

## 🚀 How to Run

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/shipping-etl-pipeline.git
cd shipping-etl-pipeline

# Start Airflow and HDFS
docker-compose up -d

# Access Airflow UI
open http://localhost:8080

# Run Dashboard
streamlit run shipping_dashboard.py
