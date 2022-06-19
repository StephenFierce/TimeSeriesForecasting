import paho.mqtt.client as mqtt_client
import numpy as np
import sched,time
import json
from datetime import datetime, timedelta
import requests
import collections

#Local IP
IP_ADDRESS = '192.168.1.24'
#Localhost
LOCAL = '127.0.0.1'
#Time Series Api Docker IP 
DOCKER = '172.17.0.2'

#REST API URL
api_url = 'http://%s:8080/api/master/asset/'%(IP_ADDRESS)
predicted = "predicted/"
datapoint = "datapoint/"
attr = "/attribute/"

#asset ID
assetID = "3xuDsmzeNPGi9X9d1mM8Zu"

#attribute name
attribute = "power"

mqtt_port = 1883
realm = 'master'
client_id = 'client124'
subscribe = "%s/%s/attribute/"%(realm,client_id)
write = "%s/%s/writeattributevalue/"%(realm,client_id)

#MQTT Username & Password
username = 'master:mqttuser'
password = 'JTnYzG5RIVlAsgIPZA2kMX1wJC1idU6u'

#Mock Cache
mock_input =  collections.deque([[130.321],[123.456],[111.321],[101.333],[122.212]])

#Log function
def on_log(client, userdata, level, buf):
    print("log: "+buf)

#Once connection is established this function subscribes to topics
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(subscribe + attribute + "/" + assetID)
    else:  
        print("Failed to connect, return code %d\n", rc)

#This function receives messages from the broker and prints to console
def on_message(client, userdata, msg):
    new_message = json.loads(msg.payload)

    # Send request to Time Series API
    PREDICT_API_URL = 'http://%s:5096/predict_json'%(DOCKER)
    predict_input = json.load(open('./3.json')) #replace with new datapoint(s)
    if 'value' in new_message['attributeState']:
        mock_input.append([new_message['attributeState']['value']])
        if (len(mock_input) >= 10):
            mock_input.popleft()
        response = requests.post(PREDICT_API_URL, json=list(mock_input))
        new_datapoints = response.json()
        print("Predicted value(s): " + str(new_datapoints))

        # Mock new datapoint 30 min in the future
        mock_datapoints = []
        for i,dp in enumerate(new_datapoints):
            mock_timestamp = int(datetime.timestamp(datetime.fromtimestamp(new_message['timestamp']/1000.0) + timedelta(minutes=i*60))*1000)
            mock_datapoints.append({
            "timestamp":  mock_timestamp,
            "value": dp[0]
            })

        # Send prediction to Open Remote instance (and delete old prediction)
        response = requests.delete(api_url + predicted + assetID + attr + attribute)
        print(str(response.status_code) + " old prediction delete OK")
        response = requests.post(api_url + predicted + assetID + attr + attribute,json=mock_datapoints)
        print(str(response.status_code) + " new predicition post OK")

def on_disconnect(client, userdata,rc=0):
    print("Disconnected result code "+str(rc))
    client.loop_stop()
    
#Set Connecting Client ID, user and pass
client = mqtt_client.Client(client_id)
client.username_pw_set(username, password)

#Linking callback functions
client.on_connect = on_connect
client.on_log = on_log
client.on_message = on_message
client.on_disconnect = on_disconnect

#Initialise connection
print("Connecting...")
client.connect(IP_ADDRESS,mqtt_port)

def disconnect():
    print("Disconnecting...")
    client.disconnect()
    client.loop_stop()

#Start listening
print("Listening...")
try:
    client.loop_forever()
except KeyboardInterrupt:
    disconnect()