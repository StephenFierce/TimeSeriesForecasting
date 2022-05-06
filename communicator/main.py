import paho.mqtt.client as mqtt_client
import ssl
import numpy as np
import sched,time
import json
import model.LSTMModel as LSTMModel
from datetime import datetime
import requests

#base url
api_url = "http://localhost:8080/api/master/asset/"
predicted = "predicted/"
datapoint = "datapoint/"
#asset ID
assetID = "6Km3L3Rpv7OitJfOGyAlLn"
attr = "/attribute/"
#attribute
attribute = "power"

broker = 'localhost'
port = 1883
subscribe = "master/client124/attribute/"
sub_attribute = "power/"
write = "master/client124/writeattributevalue/power/"
client_id = 'client124'
username = 'master:mqttuser'
password = 'nIzd43x4oosl2jeRbxit6mjmoYXuPRFR'

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
    new_datapoint = [{
        "timestamp":  datetime.fromtimestamp(new_message['timestamp']/1000.0),
        "entity_id": new_message['attributeState']['ref']['id'],
        "attribute_name": new_message['attributeState']['ref']['name'],
        "value": new_message['attributeState']['value']
     }]
    forecast,history = LSTMModel.run_model(new_datapoint)

    body = json.loads(forecast) 
    history_body = json.loads(history)
    response = requests.delete(api_url + predicted + assetID + attr + attribute)
    print(response.status_code)
    response = requests.post(api_url + predicted + assetID + attr + attribute,json=body)
    print(response.status_code)

    #delete + add historic data
    response = requests.delete(api_url + datapoint + assetID + attr + attribute)
    print(response.status_code)
    response = requests.post(api_url + datapoint + assetID + attr + attribute,json=history_body)
    print(response.status_code)

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
client.connect(broker,port)

def disconnect():
    print("Disconnecting...")
    client.disconnect()
    client.loop_stop()

s = sched.scheduler(time.time,time.sleep)

def interval_publish(sc):
    client.publish(write + assetID,payload=np.random.randint(0,1000),qos=0,retain=False)
    sc.enter(10,1,interval_publish, (sc,))

s.enter(10,1,interval_publish,(s,))


#Start listening
print("Listening...")
try:
    client.loop_start()
    while client.is_connected:
        client.publish(write + assetID,payload=np.random.randint(0,250),qos=0,retain=False)
        time.sleep(60)
except KeyboardInterrupt:
    disconnect()





