import paho.mqtt.client as mqtt_client
import numpy as np
import pandas as pd
import json
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
import dateutil.parser as duparser
import requests, os, collections
import joblib
from os.path import dirname


#Local IP
IP_ADDRESS = '145.93.100.78'
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
assetID = "3as16N7vT0PEzOvjP50OMZ"

#attribute name
attribute = "power"

mqtt_port = 1883
realm = 'master'
client_id = 'client124'
subscribe = "%s/%s/attribute/"%(realm,client_id)
write = "%s/%s/writeattributevalue/"%(realm,client_id)

#MQTT Username & Password
username = 'master:mqttuser'
password = 'buSyvqRvIViawfH4AbCyG98H8Te1mgvx'

#Mock Cache

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
    print(dirname(__file__))
    historic = pd.read_json(dirname(__file__) + '/laadpalen.json') #replace with new datapoint(s)
    historic = historic.sort_values(by='timestamp')
    #historic.sort(key=lambda x: duparser.parse(x['timestamp']))
    sampled = historic.set_index('timestamp').resample('30min').agg('mean').fillna(0)
    sampled['timestamp'] = sampled.index
    if 'value' in new_message['attributeState']:
        # Mock Cache
        mock_input =  collections.deque()
        historic_end = sampled.tail(600)
        for i,dp in enumerate(historic_end.values.tolist()):
                mock_input.append([dp[0]])


        # Predict
        mock_input.append([new_message['attributeState']['value']])
        if (len(mock_input) >= 10):
            mock_input.popleft()
        response = requests.post(PREDICT_API_URL, json=list(mock_input))
        new_datapoints = response.json()

        #scale data
        scaler = MinMaxScaler(feature_range=(historic['value'].min(),historic['value'].max()))
        scaled_data = scaler.fit_transform(new_datapoints)

        # Mock new datapoint 30 min in the future
        mock_datapoints = []
        for i,dp in enumerate(scaled_data):
            mock_timestamp = int(datetime.timestamp(datetime.fromtimestamp(new_message['timestamp']/1000.0) + timedelta(minutes=i*30))*1000)
            mock_datapoints.append({
            "timestamp":  mock_timestamp,
            "value": dp[0]
            })

        # Mock historic datapoints each 60 minutes into the past
        mock_historic = []
        date_diff = int(datetime.timestamp(datetime.now()) - datetime.timestamp(sampled.iloc[-1]['timestamp']))
        for i,dp in enumerate(sampled.values.tolist()):
            mock_timestamp = int(datetime.timestamp(pd.Timestamp(dp[1])) + date_diff)*1000
            mock_historic.append({
            "timestamp":  mock_timestamp,
            "value": dp[0]
            })

        # Send prediction to Open Remote instance (and delete old prediction)
        response = requests.delete(api_url + predicted + assetID + attr + attribute)
        print(str(response.status_code) + " old prediction delete OK")
        response = requests.post(api_url + predicted + assetID + attr + attribute,json=mock_datapoints)
        print(str(response.status_code) + " new predicition post OK")
        

        # Inserting Demo Data
        response = requests.delete(api_url + datapoint + assetID + attr + attribute)
        print(str(response.status_code) + " old demo data delete OK")
        response = requests.post(api_url + datapoint + assetID + attr + attribute,json=mock_historic)
        print(str(response.status_code) + " new demo data post OK")


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