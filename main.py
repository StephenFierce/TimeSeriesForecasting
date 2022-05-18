import paho.mqtt.client as mqtt_client
import numpy as np
import sched,time
import json
from datetime import datetime, timedelta
import requests

#base url
IP_ADDRESS = '192.168.1.24'
api_url = 'http://192.168.1.24:8080/api/master/asset/'
predicted = "predicted/"
datapoint = "datapoint/"
#asset ID
assetID = "6BtaAwik8DZbedexptenPG"
attr = "/attribute/"
#attribute
attribute = "power"

port = 1883
subscribe = "master/client124/attribute/"
sub_attribute = "power/"
write = "master/client124/writeattributevalue/power/"
client_id = 'client124'
username = 'master:mqttuser'
password = '0pFtSFY9cJlKnJX3LW8hBkg40cgxxhAN'

#Log function
def on_log(client, userdata, level, buf):
    print("log: "+buf)

#Once connection is established this function subscribes to topics
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(subscribe + sub_attribute + assetID)
    else:  
        print("Failed to connect, return code %d\n", rc)

#This function receives messages from the broker and prints to console
def on_message(client, userdata, msg):
    new_message = json.loads(msg.payload)

    # body = json.loads(forecast) 
    # history_body = json.loads(history)
    # response = requests.delete(api_url + predicted + assetID + attr + attribute)
    # print(response.status_code)
    # response = requests.post(api_url + predicted + assetID + attr + attribute,json=body)
    # print(response.status_code)

    # #delete + add historic data
    # response = requests.delete(api_url + datapoint + assetID + attr + attribute)
    # print(response.status_code)
    # response = requests.post(api_url + datapoint + assetID + attr + attribute,json=history_body)
    # print(response.status_code)

    # Send request to Time Series API
    PREDICT_API_URL = 'http://172.17.0.2:5096/predict_json'
    predict_input = json.load(open('./2.json')) #replace with new datapoint(s)
    response = requests.post(PREDICT_API_URL, json=predict_input)
    new_datapoint = response.json()
    print("Predicted value(s): " + str(new_datapoint))

    # Mock new datapoint 30 min in the future
    mock_timestamp = datetime.fromtimestamp(new_message['timestamp']/1000.0) + timedelta(minutes=30)
    mock_datapoint = [{
    "timestamp":  int(datetime.timestamp(mock_timestamp)*1000),
    "value": new_datapoint[0][0]
    }]


    # Send prediction to Open Remote instance (and delete old prediction)
    response = requests.delete(api_url + predicted + assetID + attr + attribute)
    print(str(response.status_code) + " old prediction delete OK")
    response = requests.post(api_url + predicted + assetID + attr + attribute,json=mock_datapoint)
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

#CA Certificate
#client.tls_set('/Users/stephen/cacert.pem',None,None,cert_reqs=ssl.CERT_NONE,tls_version=ssl.PROTOCOL_TLSv1_2)
#client.tls_insecure_set(True)

#Initialise connection
print("Connecting...")
client.connect(IP_ADDRESS,port)

def disconnect():
    print("Disconnecting...")
    client.disconnect()
    client.loop_stop()

s = sched.scheduler(time.time,time.sleep)

def interval_publish(sc):
    client.publish(write + assetID,payload=np.random.randint(0,1000),qos=0,retain=False)
    sc.enter(10,1,interval_publish, (sc,))

#s.enter(10,1,interval_publish,(s,))


#Start listening
print("Listening...")
try:
    client.loop_forever()
    # Publish dummy value every 60 seconds
    #client.loop_start()
    #while client.is_connected:
        #client.publish(write + assetID,payload=np.random.randint(0,250),qos=0,retain=False)
        #time.sleep(60)
except KeyboardInterrupt:
    disconnect()





