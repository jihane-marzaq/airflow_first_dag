from airflow.decorators import dag, task
from datetime import datetime
import requests 
import pandas as pd

@dag(start_date=datetime(2026,5,7),schedule='@daily',catchup=False)

def weather_dag():
    
    @task()
    def extract():
        url="https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m"
        response=requests.get(url)
        data=response.json()
        return data
    
    @task()
    def transform(data):
        times = data["hourly"]["time"]
        temps = data["hourly"]["temperature_2m"]
        # 3. Transformation → DataFrame
        df = pd.DataFrame({
            "time": times,
            "temperature": temps
        })
        return df.to_dict()
    
    @task()
    def load(df):
        df = pd.DataFrame(df)
        filename = f"/opt/airflow/dags/data/weather_{datetime.now().date()}.csv"
        
        df.to_csv(filename, index=False)
        print("✅ CSV créé avec succès !")
        
    # Pipeline
    data = extract()
    transformed_data = transform(data)
    load(transformed_data)
    



# IMPORTANT
weather_pipeline = weather_dag()