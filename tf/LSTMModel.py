
import tensorflow as tf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler

def run_model(dp):
    datapoint = pd.DataFrame(dp)
    df1 = load_json()
    sampled = format(df1,datapoint)
    forecast = test_model(sampled)
    print(forecast)
    return forecast


def load_json():
    loaded_json = pd.read_json('./laadpalen.json')
    loaded_json.sort_values('timestamp', inplace=True)
    date_diff = datetime.now() - loaded_json.iloc[-1]['timestamp']
    offset = date_diff - timedelta(seconds=60)
    loaded_json['timestamp'] = loaded_json['timestamp'] + pd.Timedelta(offset)
    return loaded_json


def format(df1,dp):
    df = pd.concat([df1, dp])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df[['timestamp', 'value']]
    # Downsample the dataset
    return df.set_index('timestamp').resample('30min').agg('first').fillna(0)


def test_model(sampled):
    #scale data
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(sampled)

    #create scaled training data
    train_length = int(round(scaled_data.shape[0]*0.8))
    train_data = scaled_data[:train_length]

    #split into x_train and y_train
    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i,0]) # Wat houdt die 60 in?
        y_train.append(train_data[i, 0])
    
    #convert the x train and y train to numpy array
    x_train, y_train = np.array(x_train), np.array(y_train)

    #reshape data
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    #build lstm model
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(tf.keras.layers.LSTM(50, return_sequences=False)) # waarom hier nog een keer en ook twee keer Dense?
    model.add(tf.keras.layers.Dense(25))
    model.add(tf.keras.layers.Dense(1))

    #compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    #train the model
    model.fit(x_train, y_train, batch_size = 1, epochs=1)

    #create the testing data set
    #create new array containing scale values from index
    test_data = scaled_data[train_length - 60:]

    #create data sets x_test and y_test
    x_test = []
    for i in range(60, len(test_data)):
        x_test.append(test_data[i-60:i, 0])

    #convert data to numpy array
    x_test = np.array(x_test)

    #reshape data
    x_test = np.reshape(x_test,(x_test.shape[0], x_test.shape[1], 1))

    #get models predicted price
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    #plot data
    train_LSTM = sampled[:train_length]
    valid_LSTM = sampled[train_length:]
    valid_LSTM['Predictions'] = predictions.copy()
    valid_LSTM = valid_LSTM[['Predictions']]
    valid_LSTM.rename(columns={'Predictions': 'value'},inplace=True)
    valid_LSTM.reset_index(inplace=True)
    sampled.reset_index(inplace=True)
    
    

    #return forecast data
    #train_LSTM.to_json(orient='records')
    return valid_LSTM.to_json(orient='records'),sampled.to_json(orient='records')
    #return train_LSTM.to_json(orient='records')




test_dp = [{
   "timestamp": "2022-02-11 18:03:58.024",
   "name": "EV Chargers",
   "attribute_name": "power",
   "value": 195.638
 }]

run_model(test_dp)