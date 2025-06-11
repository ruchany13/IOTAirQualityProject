import time
import psycopg
import os
import schedule
import requests

db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST", "postgres-service")
db_port = os.getenv("POSTGRES_PORT", "5432")

def prepare_database():
    try:
        
        conninfo = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        with psycopg.connect(conninfo) as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS data (
                        id serial PRIMARY KEY,
                        temperature_c INTEGER NOT NULL ,
                        humidity SMALLINT NOT NULL,
                        time TIMESTAMPTZ NOT NULL)
                        """)
                
            print("Veritabanı bağlantısı başarılı, tablosu hazır!")
            conn.commit()

    except psycopg.OperationalError as e:
        print(f"Bağlantı hatası: {e}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
    

# Calculate temperature and humditty data for 5 minutes
def get_data_db():
    try:
        conninfo = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        with psycopg.connect(conninfo) as conn:            
            with conn.cursor() as cur:
                
                cur.execute("SELECT * FROM data WHERE time >= NOW() - INTERVAL '5 minutes'")
                
                last_five_minutes_data=cur.fetchall()
                humidity_all=0
                temperature_c_all=0
                
                for record in last_five_minutes_data:
                    print(f"ID: {record[0]}, Sıcaklık: {record[1]}°C, Nem: {record[2]}%, Zaman: {record[3].strftime('%H:%M:%S')}")

                    humidity_all += record[1]
                    temperature_c_all += record[2]

    except psycopg.OperationalError as e:
        print(f"Bağlantı hatası: {e}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
    
    return last_five_minutes_data, humidity_all, temperature_c_all


def calculate_data(last_five_minutes_data, humidity_all, temperature_c_all):
    
    first_id = last_five_minutes_data[0][0]
    last_id = last_five_minutes_data[-1][0]
    total_id = last_id - first_id
    
    average_temperature_c = "{:.2f}".format(temperature_c_all / total_id)
    average_humidity = "{:.2f}".format(humidity_all / total_id)
    

    print("Ortalama nem:",average_humidity)
    print("Ortalama sıcaklık:", average_temperature_c)

    return average_humidity, average_temperature_c


def send_api(humidity, temperature):

    # 1. Veri göndereceğimiz endpoint'i tanımla
    API_URL = "http://127.0.0.1:8000/receive_data"
    SECRET_KEY = os.getenv("SECRET_API_KEY")

    payload = {
        "temperature": temperature,
        "humidity": humidity
    }

    headers = {
    "X-API-Key": SECRET_KEY
    }

    print(f"Aşağıdaki veri sunucuya gönderiliyor: {payload}")

    try:
        # 3. POST isteği gönder. 'json=' parametresi, sözlüğü otomatik olarak JSON'a çevirir.
        response = requests.post(API_URL, json=payload, headers=headers)
        
        # 4. Yanıtın başarılı olup olmadığını kontrol et
        if response.status_code == 200:
            # 5. Sunucunun yanıtını (bizim gönderdiğimiz verinin yansıması) al
            data = response.json()
            print("\nSunucu bağlantısı başarılı")
            print(data)
            
        else:
            print(f"Hata! Sunucudan yanıt alınamadı. Durum Kodu: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Bağlantı hatası: {e}")


def main():
    last_five_minutes_data, humidity_all, temperature_c_all = get_data_db()
    temperature, humidity = calculate_data(last_five_minutes_data, humidity_all, temperature_c_all)
    send_api(temperature, humidity)

if __name__=="__main__":
    prepare_database()
    main()

    # Every five minutes in a hour will trigger job. Because of data continuity.
    """for minute in ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"]:
        schedule.every().hour.at(f":{minute}").do(main)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
    """