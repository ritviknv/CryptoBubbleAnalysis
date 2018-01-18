import numpy as np
from numpy.linalg import norm
from scipy import interpolate
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import csv
from datetime import date, timedelta
import datetime
import calendar
import matplotlib.pyplot as plt
import analysisFunctions
import mlpy
import matplotlib.cm as cm
import dtw

#set up stock price arrays
datetimes = []
stockSums = []
counts = []
averageStockPrices = []
#set up crypto price arrays 
dates = []
btcPrices = []

#read stock prices
ifile = open('DotComHistoData.csv',"rU")
reader = csv.reader(ifile)
rownum=0
#read file
for row in reader:
	#do nothing if you're at the first row, which contains column headers
	if rownum==0:
		header=row
	else:
		datetimes.append(row[0])
		stockSums.append(float(row[1]))
		counts.append(float(row[2]))
	rownum+=1

#read btc prices
ifile2 = open('cryptoprices.csv', 'rU')
reader2 = csv.reader(ifile2)

for row2 in reader2: 
	dates.append(row2[0])
	btcPrices.append(float(row2[1]))

#average the stocks
averageStocks = analysisFunctions.averageStocks(stockSums, counts)

#remove zeros from data because they represent weekends and public holidays
zeroedData = analysisFunctions.removeZeros(averageStocks)

#finance data contains a lot of noise, so let's smoothen it by taking the weekly 5 day average of the average price of each stock
smoothenedStockData = analysisFunctions.smoothenArray(zeroedData,5)

#normalize the smoothenedAverages
normalizedStockSums = analysisFunctions.normalizeArray(smoothenedStockData)

#bitcoin prices fluctuate a lot, so let's smoothen the data by taking a 7 day average (since they're traded all week)
smoothenedBTCData = analysisFunctions.smoothenArray(btcPrices, 7)

#noramlize the smoothened BTC data
normalizedBTCPrices = analysisFunctions.normalizeArray(smoothenedBTCData)

#create numpy version of arrays
x = np.array(normalizedStockSums)
y = np.array(normalizedBTCPrices)

#compute dtw
distance, path = fastdtw(x, y, dist = euclidean)

#generate subsequent plots
analysisFunctions.plotScatterWithTwoSeries(normalizedStockSums, normalizedBTCPrices)
analysisFunctions.plotDTWCostPlot(path, x, y)
analysisFunctions.plotScatterWithFixedTrendline(path)

ifile.close()
ifile2.close()
