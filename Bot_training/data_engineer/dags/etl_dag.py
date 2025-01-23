from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from src.extraction import extract_data
from src.transformation import preprocess_data
from src.loading import load_data

# Định nghĩa DAG
dag = DAG('stock_data_pipeline', description='Pipeline xử lý dữ liệu chứng khoán',
          schedule_interval='@daily', start_date=datetime(2023, 1, 1), catchup=False)

# Định nghĩa các tác vụ trong DAG
extract_task = PythonOperator(task_id='extract_data', python_callable=extract_data.extract_data, dag=dag)
transform_task = PythonOperator(task_id='transform_data', python_callable=preprocess_data.preprocess_data, op_args=[extract_task.output], dag=dag)
load_task = PythonOperator(task_id='load_data', python_callable=load_data.load_data, op_args=[transform_task.output], dag=dag)

# Chạy các tác vụ theo thứ tự
extract_task >> transform_task >> load_task
