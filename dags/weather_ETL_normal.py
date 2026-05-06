
import requests 
import pandas as pd
from sqlalchemy import true

url="https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&daily=temperature_2m_max"

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'}
response=requests.get(url, headers=headers)
data=response.json()

# 2. Extraction
times = data["daily"]["time"]
temps = data["daily"]["temperature_2m_max"]

# 3. Transformation → DataFrame
df = pd.DataFrame({
    "time": times,
    "temperature": temps
})

# 4. Sauvegarde CSV
df.to_csv("weatherdaily2.csv", index=true)

print("✅ CSV créé avec succès !")

