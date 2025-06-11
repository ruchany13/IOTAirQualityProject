from fastapi import FastAPI
from pydantic import BaseModel

class SensorData(BaseModel):
    temperature: float
    humidity: float

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Sıcaklık ve Nem Sensörüne API'a Hoşgeldiniz."}

@app.post("/receive_data")
def receive_data(data: SensorData):
    print("Yeni veri alındı!")
    print(f"Sıcaklık: {data.temperature}°C")
    print(f"Nem: {data.humidity}%")
    
    return {"status": "success", "received_data": data }
