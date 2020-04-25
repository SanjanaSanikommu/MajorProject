import os, sys, shutil, time

from flask import Flask, request, jsonify, render_template,send_from_directory
import pandas as pd
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import urllib.request
import json
from geopy.geocoders import Nominatim

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index1.html')


@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/work.html')
def work():
    return render_template('work.html')

@app.route('/enter.html')
def enter():
    return render_template('enter.html')

@app.route('/option.html')
def about():
    return render_template('option.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/result.html', methods = ['POST'])
def predict():
    rfc = joblib.load('model/rf_model')
    print('model loaded')

    if request.method == 'POST':

        address = request.form['Location']
        geolocator = Nominatim()
        location = geolocator.geocode(address,timeout=None)
        print(location.address)
        lat=[location.latitude]
        log=[location.longitude]
        latlong=pd.DataFrame({'latitude':lat,'longitude':log})
        print(latlong)

        DT= request.form['timestamp']
        latlong['timestamp']=DT
        data=latlong
        cols = data.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        data = data[cols]

        data['timestamp'] = pd.to_datetime(data['timestamp'].astype(str), errors='coerce')
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        column_1 = data.iloc[:,0]
        DT=pd.DataFrame({"year": column_1.dt.year,
              "month": column_1.dt.month,
              "day": column_1.dt.day,
              "hour": column_1.dt.hour,
              "dayofyear": column_1.dt.dayofyear,
              "week": column_1.dt.week,
              "weekofyear": column_1.dt.weekofyear,
              "dayofweek": column_1.dt.dayofweek,
              "weekday": column_1.dt.weekday,
              "quarter": column_1.dt.quarter,
             })
        data=data.drop('timestamp',axis=1)
        final=pd.concat([DT,data],axis=1)
        X=final.iloc[:,[1,2,3,4,6,10,11]].values
        my_prediction = rfc.predict(X)
        if my_prediction[0][0] == 1:
            my_prediction='Predicted crime : Robbery'
        elif my_prediction[0][1] == 1:
            my_prediction='Predicted crime : Gambling'
        elif my_prediction[0][2] == 1:
            my_prediction='Predicted crime : Accident'
        elif my_prediction[0][3] == 1:
            my_prediction='Predicted crime : Violence'
        elif my_prediction[0][4] == 1:
            my_prediction='Predicted crime : Murder'
        elif my_prediction[0][5] == 1:
            my_prediction='Predicted crime : kidnapping'
        else:
            my_prediction='Place is safe no crime expected at that timestamp.'



    return render_template('result.html', prediction = my_prediction,loca = location.address,lati=latlong)


if __name__ == '__main__':
    app.run(debug = True)
