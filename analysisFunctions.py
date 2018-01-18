import numpy as np
from numpy.linalg import norm
from scipy.stats import f
from scipy import interpolate
from scipy.spatial.distance import euclidean
import csv
from datetime import date, timedelta
import datetime
import calendar
import matplotlib.pyplot as plt
import mlpy
import matplotlib.cm as cm
import dtw

def normalizeArray(arrayToNormalize):
	maxVal = max(arrayToNormalize)
	normedArray = [x / maxVal for x in arrayToNormalize]
	return normedArray

def averageStocks(arrayToAverage, arrayWithCounts):
	averageValues = []
	rowNumber = 0
	for i in arrayToAverage:
		if i>0:
			averageValues.append(i/arrayWithCounts[rowNumber])
		else: 
			averageValues.append(0)
		rowNumber+=1

	return averageValues

def returnArrayDifferences(arrayToFluctuate):
	growthArray = []
	index = 0
	for val in arrayToFluctuate:
		if index != len(arrayToFluctuate)-1:
			eye = arrayToFluctuate[index]
			eyePlusOne = arrayToFluctuate[index+1]
			growthArray.append(eyePlusOne - eye)

		index+=1
	return growthArray

def removeZeros(arrayToClean):
	returnArray = []
	for i in arrayToClean:
		if float(i) != 0.0:
			returnArray.append(i)
	return returnArray

def smoothenArray(arrayToSmoothen, days):
	returnArray = []
	priceSum = 0
	for i in range(0,len(arrayToSmoothen)-days+1,days):
		for j in range(0, days):
			priceSum += arrayToSmoothen[i+j]
		returnArray.append(priceSum/days)
		priceSum = 0
	return returnArray

def computePeriodogram(arrayToGeneralize, coordinate):
	omega = coordiante*2*22/7/len(arrayToGeneralize)
	n = len(arrayToGeneralize)
	imaginaryDigit = (-1)**(1/2)
	iterator = 1
	interpolatedVal = 0
	for i in arrayToGeneralize:
		interpolatedVal+=i*(exp**(imaginaryDigit*-1*omega*iterator))
		iterator += 1

	interpolatedVal *= (1/(2*pi*n))
	return interpolatedVal	

def computeRSquared(x, y, slope):
	#z = np.polyfit(x,y,1)
	z = [slope*1.000, 0.0000]
	p = np.poly1d(z)
	yhat = p(x)
	ybar = np.sum(y)/len(y)
	sstot = np.sum((y-ybar)**2)
	sse = np.sum((y-yhat)**2)
	return(1.0-sse*1.0/sstot)

def computeStandardErrorofRegression(x,y,slope):
	z = [slope*1.000, 0.0000]
	p = np.poly1d(z)
	yhat = p(x)
	return (np.sum((y-yhat)**2)/len(y))**0.5

def computeFStatistic(path):
	#split path into arrays
	x = []
	y = []
	for row in path:
		x.append((row[0]))
		y.append((row[1]))

	#compute slope of ideal trend line
	slope = float(max(y))/float(max(x))


	#generate y-hat
	z = [slope*1.000, 0.0000]
	polynomial = np.poly1d(z)
	yhat = polynomial(x)

	#generate y-bar
	ybar = np.sum(y)/len(y)

	#calculate msr and mse
	msr = np.sum((yhat-ybar)**2)
	mse = np.sum((y-yhat)**2)/(len(y)-2)

	#return f-stat
	return msr/mse

def computeStandardDeviation(x):
	std = np.sum((x-average(x)))	

def convertToString(arrayToConvert):
	returnArray = []
	for row in arrayToConvert:
		returnArray.append(str(row))

	return returnArray

#Plotting related functions
def plotScatterWithTwoSeries(y1, y2):

	#create dummy x values, to fix the start points to each other
	dummyXStockPoints = []
	iterate = 0
	for i in y1:
		dummyXStockPoints.append(iterate)
		iterate+=1

	#create dummy x values, to fix the start points to each other
	dummyXBTCPoints = []
	iterate2 = 0
	for i in y2:
		dummyXBTCPoints.append(iterate2)
		iterate2+=1

	plt.plot(dummyXStockPoints, y1, 'c', linewidth=2.0, alpha = 0.5,  markeredgecolor='g', markeredgewidth = 0.0, label = "Normalized 5-Day Ave. Stock Prices")
	plt.plot(dummyXBTCPoints, y2, 'y', linewidth=2.0, alpha = 0.5,  markeredgecolor='g', markeredgewidth = 0.0, label = "Normalized 7-Day Ave. BTC Prices")

	plt.suptitle("Normalized, Smoothened Stock and BTC Prices vs. Time", fontsize=15)
	plt.ylabel("Normalized Averaged Prices")
	plt.xlabel("Time")
	plt.legend(loc='upper left', ncol=1, fontsize = 10)
	plt.show()

def plotDTWCostPlot(path, x, y):
	xPath = []
	yPath = []
	for row in path:
		xPath.append(row[0])
		yPath.append(row[1])

	w, h = len(x), len(y);
	Matrix = [[0 for a in range(w)] for b in range(h)] 

	for i in range(0, len(x)):
		for j in range(0, len(y)):
			Matrix[j][i] = (((x[i]*x[i])-(y[j]*y[j]))**2)**(1/4.0)


	fig = plt.figure(1)
	ax = fig.add_subplot(111)
	plot1 = plt.imshow(Matrix, origin = 'lower', cmap = cm.YlGn, interpolation = 'nearest')
	plot2 = plt.plot(xPath, yPath, 'black', linewidth = 2.0, label = "DTW Lowest Cost Path")
	plt.colorbar(label = "Distances")
	plt.legend(loc='upper left', ncol=1, fontsize = 10)
	plt.ylabel("BTC Time Series Indices")
	plt.xlabel("Stock Price Time Series Indices")
	plt.suptitle("DTW Distances and Lowest Cost Path", fontsize=15)
	xlim = ax.set_xlim((0, 131))
	ylim = ax.set_ylim((0, 209))

	plt.show()

def plotScatterWithTrendline(path):

	x = []
	y = []
	for row in path:
		x.append(row[0])
		y.append(row[1])
	z = np.polyfit(x, y, 1)
	p = np.poly1d(z)
	rsquared = computeRSquared(x, y)

	plt.plot(x, y,'red', x, p(x),"orange", linewidth=2.0,markeredgecolor='c', markeredgewidth = 0.0, markersize=3.5, alpha = 0.5)
	plt.xlabel("BTC Indices")
	plt.ylabel("Stock Indices")
	rsquared = "R-Squared Value = " + str(rsquared) + "\nF(x) = " + str(z[0]) + "x + " + str(z[1])
	plt.text(20, 150, rsquared, fontsize = 11)
	plt.suptitle("DTW Path and Fitted Plot", fontsize=15)
	plt.show()

def plotScatterWithFixedTrendline(path):
	x = []
	y = []
	for row in path:
		x.append((row[0]))
		y.append((row[1]))

	slope = float(max(y))/float(max(x))

	fixedTrendLineStringValues = []
	for xVal in x:
		yVal = slope*float(xVal)
		fixedTrendLineStringValues.append(str(yVal))

	rsquared = computeRSquared(x, y, slope)
	standardErrorOfRegression = computeStandardErrorofRegression(x, y, slope)

	plt.plot(x, y,'red', linewidth=2.0,markeredgecolor='c', markeredgewidth = 0.0, markersize=3.5, alpha = 0.5, label = "DTW Path")
	plt.plot(x, fixedTrendLineStringValues,"orange", linewidth=2.0,markeredgecolor='c', markeredgewidth = 0.0, markersize=3.5, alpha = 0.5, label = "Fixed Trend Line")
	plt.legend(loc = 'upper left')
	plt.xlabel("BTC Indices")
	plt.ylabel("Stock Indices")
	rsquared = "R-Squared Value = " + str(rsquared) + "\nStd. Error of Regression = " + str(standardErrorOfRegression) +"\nF(x) = " + str(slope) + "x"
	plt.text(20, 150, rsquared, fontsize = 11)
	plt.suptitle("DTW Path and Fitted Plot", fontsize=15)
	plt.show()


