import influxdb_client
from influxdb_client import Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from Utils.Utils import colorPrinter
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
        |> filter(fn: (r) => r._measurement == "Measurement" and r.sensorId == "{sensorId}")
        |> sort(columns: ["_time"], desc: true)
        """
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
    
    def periodMin(self, period, sensorId):
        result = {}
        query = f"""
            from(bucket: "READINGS")
            |> range(start: -{period})
            |> filter(fn: (r) => r["_measurement"] == "Measurement")
            |> filter(fn: (r) => r["sensorId"] == "{sensorId}")
            |> aggregateWindow(every: {period}, fn: min)
            |> first()
            |> yield(name: "min")
            """
        tables = self.query_api.query(query, org="IOTPolito")
        for table in tables:
            for record in table.records:
                print('Record:', record['result'],record['_value'])
                # result = {record['result']: record['_value']}
                result = record['_value']
        return result

    def periodMax(self, period, sensorId):
        result = {}
        query = f"""
            from(bucket: "READINGS")
            |> range(start: -{period})
            |> filter(fn: (r) => r["_measurement"] == "Measurement")
            |> filter(fn: (r) => r["sensorId"] == "{sensorId}")
            |> aggregateWindow(every: {period}, fn: max)
            |> first()
            |> yield(name: "max")
            """
        tables = self.query_api.query(query, org="IOTPolito")
        for table in tables:
            for record in table.records:
                print('Record:', record['result'],record['_value'])
                # result = {record['result']: record['_value']}
                result = record['_value']
        return result

    def periodMean(self, period, sensorId):
        result = {}
        query = f"""
            from(bucket: "READINGS")
            |> range(start: -{period})
            |> filter(fn: (r) => r["_measurement"] == "Measurement")
            |> filter(fn: (r) => r["sensorId"] == "{sensorId}")
            |> aggregateWindow(every: {period}, fn: mean)
            |> first()
            |> yield(name: "mean")
            """
        tables = self.query_api.query(query, org="IOTPolito")
        for table in tables:
            for record in table.records:
                print('Record:', record['result'],record['_value'])
                # result = {record['result']: record['_value']}
                result = record['_value']
        return result
    
    def lastValue(self, sensorId, period='30m'):
        result = {}
        query = f"""
        from(bucket: "READINGS")
        |> range(start: -{period})
        |> filter(fn: (r) => r["_measurement"] == "Measurement")
        |> filter(fn: (r) => r["sensorId"] == "{sensorId}")
        |> last()
        """
        tables = self.query_api.query(query, org="IOTPolito")
        for table in tables:
            for record in table.records:
                print('Record:', record['result'],record['_value'])
                # result = {record['result']: record['_value']}
                result = record['_value']
        return result



    
    def readAllSensorsData(self,sensorIds, period='30m'):
        result = {}
        for sensorId in sensorIds:
            # colorPrinter('Min', 'yellow')
            # print(sensorId, self.periodMin(period, sensorId))
            # colorPrinter('Max', 'yellow')
            # print(sensorId, self.periodMax(period, sensorId))
            # colorPrinter('Mean', 'yellow')
            # print(sensorId, self.periodMean(period, sensorId))
            counter = 0
            type = None
            unit = None
            records = []
            query = f"""from(bucket: "READINGS")
            |> range(start: -{period})
            |> filter(fn: (r) => r._measurement == "Measurement" and r.sensorId == "{sensorId}")
            |> sort(columns: ["_time"], desc: true)
            """
            tables = self.query_api.query(query, org="IOTPolito")
            for table in tables:
                for record in table.records:
                    # print('Record:', record)
                    if counter == 0:
                        type = record['type']
                        unit = record['unit']
                        counter += 1
                    records.append({"value": record['_value'], "time": record['_time'].isoformat()})
                result[sensorId] = {"records": records, "type": type, "unit": unit, "sensorId": sensorId, "period": period, "min": self.periodMin(period, sensorId), "max": self.periodMax(period, sensorId), "mean": self.periodMean(period, sensorId), "lastValue": self.lastValue(sensorId, period)}

        return result

    def readCommands(self, sensorId, period='30m'):
        result = []
        query = f"""from(bucket: "READINGS") 
            |> range(start: -{period}) 
            |> filter(fn: (r) => r["_measurement"] == "Command" and r["type"] == "air_condition" and r["sensorId"] == "{sensorId}")
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            |> keep(columns: ["_time", "temperature", "humidity", "status", "actionType"])
            |> sort(columns: ["_time"], desc: true)
            """
        tables = self.query_api.query(query, org="IOTPolito")
        for table in tables:
            for record in table.records:
                print('Record:', record)
                result.append({"time": str(record['_time']),"temperature": record['temperature'], "humidity": record['humidity'], "status": record['status'], "actionType": record['actionType']})
        return {"records": result, "sensorId": sensorId, "period": period}
        # return {}



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

