from influxdb import InfluxDBClient
# export INFLUXDB_TOKEN=_Mrrxqa5TGx_QHy2ChmtHVpJB2nf-eV0itB6NS7FX7mye2cSXpvheLCN-FNXo4s5KXm_T_1QQzRIlmNUDAoXwA==
#deffault client object is : InfluxDBClient('localhost', 8086, 'admin', 'password', 'iot')

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = '_Mrrxqa5TGx_QHy2ChmtHVpJB2nf-eV0itB6NS7FX7mye2cSXpvheLCN-FNXo4s5KXm_T_1QQzRIlmNUDAoXwA=='
org = "IOTPolito"
url = "http://localhost:8086"
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# token = os.environ.get("INFLUXDB_TOKEN")

bucket="testdb"

write_api = client.write_api(write_options=SYNCHRONOUS)
   
for value in range(5):
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="IOTPolito", record=point)
  time.sleep(1) # separate points by 1 second


  import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN")
org = "IOTPolito"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)



query_api = client.query_api()

query = """from(bucket: "testdb")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
tables = query_api.query(query, org="IOTPolito")

for table in tables:
  for record in table.records:
    print(record)



query_api = client.query_api()

query = """from(bucket: "testdb")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "measurement1")
  |> mean()"""
tables = query_api.query(query, org="IOTPolito")

for table in tables:
    for record in table.records:
        print(record)