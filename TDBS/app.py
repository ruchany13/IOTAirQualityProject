import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time
token = "my-super-secret-auth-token"
org = "my-org"
url = "http://lab.ruchan.local:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="my-bucket"
write_api = client.write_api(write_options=SYNCHRONOUS)
for i in range(0,100):
  p = influxdb_client.Point("sensor_data").tag("server", "k3s").field("temperature", 24.0).field("humidity", i)
  write_api.write(bucket=bucket, org=org, record=p)
  time.sleep(1)


# Query script
query_api = client.query_api()
query = 'from(bucket:"my-bucket")\
|> range(start: -3m)\
|> filter(fn:(r) => r._measurement == "sensor_data")\
|> filter(fn:(r) => r.server == "k3s")\
|> filter(fn: (r) => r["_field"] == "humidity" or r["_field"] == "temperature")\
|> mean()'
result = query_api.query(org=org, query=query)

results = []
for table in result:
    for record in table.records:
        field_data=(record.get_field())
        value_data=(record.get_value())
        if field_data == "temperature":
          print("temperature:",value_data)
        elif field_data == "humidity":
          print("humidity:",value_data)

          
        


        

