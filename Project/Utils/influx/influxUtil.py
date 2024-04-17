import influxdb_client
from influxdb_client import Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import time

class InfluxDBManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_client()
        return cls._instance
    
    def getInstance(self):
        return self._instance

    def _initialize_client(self):
        token = 'nVzRyaR42v8EzZfSiP_hiIDWZYTeJ8jwRY8l3-ubHvg0s7mhUSN8FDM8-B6x12oq3Ms8uf6xLsFWpUYOiC1sRw=='
        org = "IOTPolito"
        url = "http://localhost:8086"
        self.urlAddress = url
        self.bucketName = "READINGS"
        self.orgName = org
        self.client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
        self.delete_api = self.client.delete_api()
        self.Point = Point

    def writeData(self, point):
        print('Called->',point)
        self.write_api.write(bucket=self.bucketName, org= self.orgName, record=point)
        self.write_api.close()

    # def readData(self, measurement, tags, fields):
    #     query = """from(bucket: "READINGS")
    #     |> range(start: -10m)
    #     |> filter(fn: (r) => r._measurement == "measurement1")"""
    #     tables = self.query_api.query(query, org="IOTPolito")
    #     for table in tables:
    #         print(len(table.records))
    #         for record in table.records:
    #             print(record)

    # def deleteData(self, measurement, tags, fields):
    #     self.delete_api.delete(start=0, stop=0, predicate='r._measurement == "measurement1"', bucket="READINGS", org="IOTPolito")
# Point =Point
# # Usage
# if __name__ == "__main__":
#     manager = InfluxDBManager()

#     for i in range(100):
#         point = (
#             manager.Point("House1")
#             .tag("room", "1")
#             .tag("sensorId", "21")
#             .tag("type", "Temperature")
#             .field("value", random.randint(0, 45))
#             .field("status", random.randint(0, 1))
#         )
#         manager.writeData(point)
#         time.sleep(1)

