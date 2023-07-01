import logging
import pickle
import io
import base64

from flask_pymongo import pymongo
from flask import Flask, request, jsonify, send_file
import pandas as pd
import numpy as np
from flask import render_template
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from statsmodels.tsa.stattools import adfuller
from pandas.plotting import autocorrelation_plot
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
import statsmodels.api as sm
from pandas.tseries.offsets import DateOffset


con_string = "mongodb+srv://ssdhushyanth2003:ssd123@sales.ogizm8k.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_string)

db = client.get_database('data')

user_collection = pymongo.collection.Collection(db, 'user')
print("MongoDB connected Successfully")


def project_api_routes(endpoints):
    
    @endpoints.route('/register-user', methods=['POST'])
    def register_user():
        resp = {}
        try:
            username = request.json['username']
            email = request.json['email']
            password = request.json['password']
            
            user_collection.insert_one({
                "username": username,
                "email": email,
                "password": password
            })
            
            print("User Data Stored Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Stored Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return jsonify(resp)


    @endpoints.route('/login',methods=['post'])
    def login():
        resp = {}
        try:
            username = request.json['username']
            password = request.json['password']
        
            user = user_collection.find_one({"username": username})
        
            if user is None:
                raise Exception("Invalid username or password")
        
            if user['password'] != password:
                raise Exception("Invalid username or password")
        
            resp['status'] = {
                "statusCode": "200",
                "statusMessage": "User Authenticated Successfully."
            }
        
        except Exception as e:
            print(e)
            resp['status'] = {
                "statusCode":"400",
                "statusMessage": str(e)
            }
    
        return jsonify(resp)
    
    @endpoints.route('/file', methods=['POST','GET'])
    def upload_file():
        # Load data from uploaded CSV file
        file = request.files['file']
        season=request.form.get('season')
        m = int(request.form.get('number'))
        y=1   
        w=1
        df = pd.read_csv(file, parse_dates=['Month'], index_col='Month')
        df = df.rename(columns={'Sales': 'y'}).reset_index()
        df = df[['Month', 'y']]
        df.dropna()
        df.columns=["Month","Sales"]
        df['Month'] = pd.to_datetime(df['Month'])
        df.set_index('Month', inplace=True)
        df['Sales'] = pd.to_numeric(df['Sales'].str.replace(',', ''))

        df.dropna()
        df.dropna(inplace=True)
        test_result = adfuller(df['Sales'])

        #Ho: It is non stationary
        #H1: It is stationary
        model=ARIMA(df['Sales'],order=(1,1,1))
        model_fit=model.fit()
        model_fit.summary()
        df['forecast']=model_fit.predict(start=104,end=175,dynamic=True)
        df[['Sales','forecast']].plot(figsize=(12,8))

        model=sm.tsa.statespace.SARIMAX(df['Sales'],order=(1, 1, 1),seasonal_order=(1,1,1,12))
        results=model.fit()



        df['forecast']=results.predict(start=104,end=175,dynamic=True)
        df[['Sales','forecast']].plot(figsize=(12,8))

        future_dates=[df.index[-1]+ DateOffset(months=x)for x in range(0,48)]

        future_datest_df=pd.DataFrame(index=future_dates[1:],columns=df.columns)
        future_datest_df.tail()

        future_df=pd.concat([df,future_datest_df])

        if(season=='m'):
            m=m*4
            future_df['predicted'] = results.predict(start = 104, end =m+104, dynamic= True)  
            future_df[['Sales', 'predicted']].plot(figsize=(12, 8))  
        elif(season=='y'):
            y=m*12
            future_df['predicted'] = results.predict(start = 104, end =y+104, dynamic= True)  
            future_df[['Sales', 'predicted']].plot(figsize=(12, 8)) 
        elif(season=='w'):
            w=m
            future_df['predicted'] = results.predict(start = 104, end =w+104, dynamic= True)  
            future_df[['Sales', 'predicted']].plot(figsize=(12, 8)) 


        

        

        
        # Generate the plot
        fig = Figure()
        ax = fig.add_subplot(111)
        ax.plot(df.index, df['Sales'])
        ax.set_xlabel('Month')
        ax.set_ylabel('Sales')
        ax.set_title('Sales Over Time')

        # Render the plot as a PNG image
        canvas = FigureCanvas(fig)
        output = io.BytesIO()
        future_df[['Sales', 'predicted']].plot(figsize=(12, 8))
        plt.savefig(output, format='png')
        encoded_image = base64.b64encode(output.getvalue()).decode('utf-8')
        return jsonify(plot=encoded_image)
          




    return endpoints