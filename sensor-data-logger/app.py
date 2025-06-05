import time
import board
import adafruit_dht
import psycopg
import datetime
import os

#GPIO 10 pini (s yazısının yanındaki pin) -> 5v -> grd
sensor = adafruit_dht.DHT11(board.D10)

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
                        time TIMESTAMP NOT NULL)
                        """)
                
            print("Veritabanı bağlantısı başarılı, tablosu hazır!")
            conn.commit()

    except psycopg.OperationalError as e:
        print(f"Bağlantı hatası: {e}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

def send_data_db(temperature, humidity, time):
    try:
        conninfo = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        with psycopg.connect(conninfo) as conn:            
            with conn.cursor() as cur:
                sql = "INSERT INTO data (temperature_c, humidity, time) VALUES (%s, %s, %s)"
                cur.execute(sql, (temperature, humidity, time))

    except psycopg.OperationalError as e:
        print(f"Bağlantı hatası: {e}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

prepare_database()

while True:
    try:
        temperature_c = sensor.temperature
        #temperature_f = temperature_c * (9 / 5) + 32
        humidity = sensor.humidity
        x = datetime.datetime.now()
        current_time=x.strftime("%Y-%m-%d %H:%M:%S")
        print(current_time, "Sıcaklık={0:0.1f}ºC, Nem={1:0.1f}%".format(temperature_c, humidity))
        send_data_db(temperature_c, humidity, current_time)
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        sensor.exit()
        raise error

    time.sleep(1.0)


