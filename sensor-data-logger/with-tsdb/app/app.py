import time, os, board
import adafruit_dht
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


token = os.environ['TOKEN']
org = os.environ['ORG']
url = os.environ['HOST']
bucket = os.environ['BUCKET']

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)


#GPIO 10 pini (s yazısının yanındaki pin) -> 5v -> grd
sensor = adafruit_dht.DHT11(board.D10)

while True:
    try:
        temperature_c = sensor.temperature
        #temperature_f = temperature_c * (9 / 5) + 32
        humidity = sensor.humidity
        print("Sıcaklık={0:0.1f}ºC, Nem={1:0.1f}%".format(temperature_c, humidity))
        p = influxdb_client.Point("sensor_data").tag("server", "k3s").field("temperature", temperature_c).field("humidity", humidity)
        write_api.write(bucket=bucket, org=org, record=p)

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    
    except Exception as error:
        sensor.exit()
        raise error

    time.sleep(1.0)

          
