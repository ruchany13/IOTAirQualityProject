from fastapi import FastAPI, Depends, Security, HTTPException
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from starlette import status
import os

class SensorData(BaseModel):
    temperature: float
    humidity: float

app = FastAPI()

api_key_header = APIKeyHeader(name="X-API-Key")

API_KEY = os.getenv("SECRET_API_KEY")

def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    Gelen isteğin başlığındaki anahtarı kontrol eden bağımlılık.
    """
    if api_key_header == API_KEY:
        return api_key_header
    else:
        # Eğer anahtar yanlışsa, 403 Forbidden hatası fırlat.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    


@app.get("/")
def read_root():
    return {"message": "Sıcaklık ve Nem Sensörüne API'a Hoşgeldiniz."}

@app.post("/receive_data")
def receive_data(data: SensorData, api_key: str = Depends(get_api_key)):
    print("Yeni veri alındı!")
    print(f"Sıcaklık: {data.temperature}°C")
    print(f"Nem: {data.humidity}%")
    
    return {"status": "success", "received_data": data }
