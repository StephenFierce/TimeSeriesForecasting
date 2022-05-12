import tensorflow as tf
import os
import json
from sklearn.preprocessing import MinMaxScaler


PATH =  os.path.expanduser("~/Documents/models/0.1")
new_model = tf.keras.models.load_model(PATH)

PREDICT_DATA = os.path.expanduser("~/Documents/models/predictdata/1.json")
f = open(PREDICT_DATA)
data = json.load(f)
prediction = new_model.predict(data)

scaler = MinMaxScaler(feature_range=(0,1))

prediction = scaler.inverse_transform(prediction)

print(prediction)
