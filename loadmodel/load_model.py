import tensorflow as tf
import os
import json

PATH =  os.path.expanduser("~/Documents/models/0.1")
classifier = tf.keras.models.load_model(PATH)

PREDICT_DATA = os.path.expanduser("~/Documents/models/predictdata/1.json")
f = open(PREDICT_DATA)
data = json.load(f)
prediction = classifier.predict(data)

print(prediction[:10])

