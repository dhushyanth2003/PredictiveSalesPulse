import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from pandas.plotting import autocorrelation_plot
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
import statsmodels.api as sm
import pickle

##from google.colab import files
#uploaded = files.upload()

df = pd.read_csv('fore.csv', parse_dates=['Month'], index_col='Month')

df = df.rename(columns={'Sales': 'y'}).reset_index()
df = df[['Month', 'y']]

##print(df)
df.dropna()

df.columns=["Month","Sales"]
##df.head()

df['Month']=pd.to_datetime(df['Month'])

df.set_index('Month',inplace=True)

df['Sales'] = pd.to_numeric(df['Sales'].str.replace(',', ''))

df.plot()

df.dropna()

df.dropna(inplace=True)
test_result = adfuller(df['Sales'])

##test_result

#Ho: It is non stationary
#H1: It is stationary

def adfuller_test(sales):
    result=adfuller(sales)
    labels = ['ADF Test Statistic','p-value','#Lags Used','Number of Observations Used']
    for value,label in zip(result,labels):
        print(label+' : '+str(value) )
    if result[1] <= 0.05:
        print("strong evidence against the null hypothesis(Ho), reject the null hypothesis. Data has no unit root and is stationary")
    else:
        print("weak evidence against null hypothesis, time series has a unit root, indicating it is non-stationary ")
    

adfuller_test(df['Sales'])

df['Sales First Difference'] = df['Sales'] - df['Sales'].shift(1)

##df['Sales']

df['Sales'].shift(1)

adfuller_test(df['Sales First Difference'].dropna())

df['Seasonal First Difference']=df['Sales']-df['Sales'].shift(12)

df['Sales'].shift(12)

df.head(14)


## Again test dickey fuller test
adfuller_test(df['Seasonal First Difference'].dropna())

df['Seasonal First Difference'].plot()

autocorrelation_plot(df['Sales'])
#plt.show()

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(df['Seasonal First Difference'].iloc[13:],lags=40,ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(df['Seasonal First Difference'].iloc[13:],lags=40,ax=ax2)

model=ARIMA(df['Sales'],order=(1,1,1))
model_fit=model.fit()


df['forecast']=model_fit.predict(start=90,end=103,dynamic=True)
df[['Sales','forecast']].plot(figsize=(12,8))

model=sm.tsa.statespace.SARIMAX(df['Sales'],order=(1, 1, 1),seasonal_order=(1,1,1,12))
results=model.fit()

df['forecast']=results.predict(start=90,end=103,dynamic=True)
df[['Sales','forecast']].plot(figsize=(12,8))

from pandas.tseries.offsets import DateOffset
future_dates=[df.index[-1]+ DateOffset(months=x)for x in range(0,48)]

future_datest_df=pd.DataFrame(index=future_dates[1:],columns=df.columns)

future_df=pd.concat([df,future_datest_df])

future_df['predicted'] = results.predict(start = 100, end = 175, dynamic= True)  
prediction=future_df[['Sales', 'predicted']].plot(figsize=(12, 8)) 

pickle.dump(prediction,open("model.pkl","wb"))