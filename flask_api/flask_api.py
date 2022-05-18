import tensorflow as tf
from flask import Flask, request, jsonify
from flasgger import Swagger
import joblib

app=Flask(__name__)
Swagger(app)
PATH =  "/usr/app/models/0.1"
classifier = tf.keras.models.load_model(PATH)
scaler = joblib.load(PATH + "/scaler.save")

@app.route('/')
def welcome():
    return "Welcome to the time series forecasting web API"

@app.route('/predict')
def predict_time_series():
    """Lets's predict with a GET request with URL parameters!
    ---
    get:
        description: Get predition from json input
        responses:
            200:
                description: The predicted values
    """

    timestamp_value_array = request.get_json('values')
    #scaled_data = scaler.fit_transform(timestamp_value_array)
    prediction = classifier.predict(timestamp_value_array)
    return "The predicted values are: " + str(prediction)

@app.route('/predict_json',methods=["POST"])
def predict_time_series_json():
    """Lets's predict with a json POST request!
    ---
    post:
        description: Get predition from json input
        parameters:
          - in: body
            name: body
            required: true
        responses:
            200:
                description: The predicted values in JSON
    """
    data = request.json
    #reshaped = data.reshape(-1,1)
    #scaled_data = scaler.fit_transform(reshaped)
    prediction = classifier.predict(data)    
    return jsonify(prediction.tolist())


if __name__=='__main__':
    app.run(host='0.0.0.0',port='5096')