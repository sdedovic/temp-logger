from influxdb import InfluxDBClient
import requests
import time, datetime


def setup():
    client.create_database('readings')
    client.create_database('metrics')
    client.switch_database('readings')


def createTempReading(temp):
    return [
        {
            "measurement": "temperature",
            "tags": {
                "device": "particle-core-1",
                "region": "test"
            },
            "time": timestampToDatetime(time.time()),
            "fields" : {
                "value": temp
            }
        }
    ]


def createMetric(url, code, msg):
    return [
        {
        "measurement": "request-error",
            "tags": {
                "device": "particle-core-1",
                "region": "test"
            },
            "time": timestampToDatetime(time.time()),
            "fields" : {
                "status": code,
                "reason": msg
            }
        }
    ]


def timestampToDatetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%SZ')


def getTemp():
    url = 'https://api.particle.io/v1/devices/54ff6f066678574948570267/temperature?access_token=747970f6e59a7f3959dea71722ca55d124befaaa'
    r = requests.get(url)
    if r.status_code is not 200:
        client.write_points(createMetric(url, r.status_code, r.text), database='metrics')
    else:
        resp = r.json()
        return resp['result']

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')

setup()

while True:
    temp = getTemp()
    reading = createTempReading(temp)
    client.write_points(reading, database='readings')
    time.sleep(5)
