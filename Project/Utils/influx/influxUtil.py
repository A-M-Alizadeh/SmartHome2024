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
        try:
            print('Called->',point)
            self.write_api.write(bucket=self.bucketName, org= self.orgName, record=point)
            self.write_api.close()
        except Exception as e:
            print(f'Error writing data {e}')

    def readSensorData(self, sensorId, period='30m'):
        counter = 0
        type = None
        unit = None
        records = []
        print('Reading data=========================================')
        query = f"""from(bucket: "READINGS")
        |> range(start: -{period})
        |> filter(fn: (r) => r._measurement == "Measurement" and r.sensorId == "{sensorId}")"""
        tables = self.query_api.query(query, org="IOTPolito")
        for table in tables:
            for record in table.records:
                if counter == 0:
                    type = record['type']
                    unit = record['unit']
                    counter += 1
                print(record)
                records.append({"value": record['_value'], "time": record['_time'].isoformat()})
        return {"records": records, "type": type, "unit": unit, "sensorId": sensorId, "period": period}
    
    def readAllSensorsData(self,sensorIds, period='30m'):
        result = {}
        for sensorId in sensorIds:
            counter = 0
            type = None
            unit = None
            records = []
            print(f'Reading data for sensor {sensorId} =========================================')
            query = f"""from(bucket: "READINGS")
            |> range(start: -{period})
            |> filter(fn: (r) => r._measurement == "Measurement" and r.sensorId == "{sensorId}")"""
            tables = self.query_api.query(query, org="IOTPolito")
            for table in tables:
                for record in table.records:
                    if counter == 0:
                        type = record['type']
                        unit = record['unit']
                        counter += 1
                    records.append({"value": record['_value'], "time": record['_time'].isoformat()})
                result[sensorId] = {"records": records, "type": type, "unit": unit, "sensorId": sensorId, "period": period}
        return result

    def readCommands(self, sensorId, period='30m'):
        counter = 0
        unit = None
        type = None
        records = []
        query = f"""from(bucket: "READINGS")
        |> range(start: -{period})
        |> filter(fn: (r) => r._measurement == "Measurement" and r.sensorId == "{sensorId}")"""
        tables = self.query_api.query(query, org="IOTPolito")
        for table in tables:
            for record in table.records:
                if counter == 0:
                    type = record['type']
                    unit = record['unit']
                    counter += 1
                print('---> ',record)
                records.append({"value": record['_value'], "time": record['_time'].isoformat(), "fields": record['_field']})
        return {"records": records, "type": type, "unit": unit, "sensorId": sensorId, "period": period}



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

