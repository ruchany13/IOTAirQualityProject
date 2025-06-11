import time
import board
import psycopg
import datetime
import os

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
                
                cur.execute("SELECT * FROM data WHERE time >= NOW() - INTERVAL '5 minutes' ORDER BY time DESC")
                
                
                last_five_minutes_data=cur.fetchall()
                print(type(last_five_minutes_data))
                humidity=0
                temperature_c=0
                
                for record in last_five_minutes_data:
                    print(f"ID: {record[0]}, Sıcaklık: {record[1]}°C, Nem: {record[2]}%, Zaman: {record[3].strftime('%H:%M:%S')}")

                humidity += record[1]
                temperature_c += record[2]


    except psycopg.OperationalError as e:
        print(f"Bağlantı hatası: {e}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")


prepare_database()
get_data_db()