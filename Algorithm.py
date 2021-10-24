# Using dual moving average crossover to determine buy or sell stock.

# Import libraries. 
import pandas as pd
import numpy as np 
from datetime import datetime
import matplotlib.pyplot as plt 
plt.style.use('fivethirtyeight')

# Load data.
from google.colab import files 
uploaded = files.upload()

# Store data.
TSLA = pd.read_csv("TSLA.csv")
# Show data.
TSLA

# Visualize the data.
plt.figure(figsize = [12.5, 6])
# Choose what you want to plot.
plt.plot(TSLA["Adj Close"], label = "TSLA")
# Remaining sections of the graph.
plt.title("TSLA Adjusted Close Price History")
plt.xlabel("June 29th, 2010 - February 3rd, 2020")
plt.ylabel("Adjusted Close Price USD($)")
plt.legend(loc = "upper left")
plt.show()

# Create a simple moving average with a 30 day window (SMA = simple moving average). pd.DataFrame creates
# the data frame for making it happen.
SMA30 = pd.DataFrame()
# List columns
SMA30["Adj Close"] = TSLA["Adj Close"].rolling(window=30).mean() 
# Show data                                           
SMA30

# Create a simple moving 100 day average
SMA100 = pd.DataFrame()
SMA100["Adj Close"] = TSLA["Adj Close"].rolling(window= 100).mean()
SMA100

# Visualize the data, using SMA30 and SMA100.
plt.figure(figsize = [12.5, 6])
plt.plot(TSLA["Adj Close"], label = "TSLA")
plt.plot(SMA30['Adj Close'], label = "SMA30")
plt.plot(SMA100['Adj Close'], label = "SMA100")
plt.title("TSLA Adjusted Close Price History")
plt.xlabel("June 29th, 2010 - February 3rd, 2020")
plt.ylabel("Adjusted Close Price USD($)")
plt.legend(loc = "upper left")
plt.show() 

# New dataframe to store all data. 
data = pd.DataFrame()
data["TSLA"] = TSLA['Adj Close']
data['SMA30'] = SMA30['Adj Close']
data['SMA100'] = SMA100['Adj Close']
data

# Create a function to signal when to buy and sell the asset
def buy_sell(data):
  sigPriceBuy = []
  sigPriceSell = []
  flag = -1

  for i in range(len(data)):
    if data['SMA30'][i] > data['SMA100'][i]:
      if flag != 1:
        sigPriceBuy.append(data['TSLA'][i])
        sigPriceSell.append(np.nan) #do nothing
        flag = 1
      else:
        sigPriceBuy.append(np.nan)
        sigPriceSell.append(np.nan)
    elif data['SMA30'][i] < data['SMA100'][i]:
      if flag != 0:
          sigPriceBuy.append(np.nan)
          sigPriceSell.append(data['TSLA'][i])
          flag = 0
      else:
          sigPriceBuy.append(np.nan)
          sigPriceSell.append(np.nan)
    else:
          sigPriceBuy.append(np.nan)
          sigPriceSell.append(np.nan)
  return (sigPriceBuy, sigPriceSell)

  # Store the buy and sell data into a variable.
buy_sell = buy_sell(data)
data['Buy_Signal_Price'] = buy_sell[0]
data['Sell_Signal_Price'] = buy_sell[1]
# Show the data.
data

# Visualize the data and the strategy to buy and sell the stock.
plt.figure(figsize=(12.5, 6))
plt.plot(data['TSLA'], label = 'TSLA', alpha = 0.3)
plt.plot(data['SMA30'], label = 'SMA30', alpha = 0.3)
plt.plot(data['SMA100'], label = 'SMA100', alpha = 0.3)
plt.scatter(data.index, data['Buy_Signal_Price'], label = "Buy", marker = "^", color = "green")
plt.scatter(data.index, data["Sell_Signal_Price"], label = "Sell", marker = "v", color = "red")
plt.title("Tesla Adj. Close Price History Buy & Sell Signals")
plt.xlabel("June 29th, 2010 - February 3rd, 2020")
plt.ylabel("Adjusted Close Price USD($)")
plt.legend(loc = "upper left")
plt.show() 
