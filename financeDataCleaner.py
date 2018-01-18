import numpy as np
from scipy import interpolate
import csv
from datetime import date, timedelta
import datetime
import calendar
import matplotlib.pyplot as plt

#functions
def takeAverage(array1, array2):
	average = []
	rownum = 0
	for i in array1:
		if not array1[rownum] or not array2[rownum]:
			average.append(0)
		else:
			average.append(array1[rownum]/array2[rownum])
		rownum+=1
	return average

#global variables
days = []
datetimes = []
val = []
counts = []
start = date(1997,8, 5)
end = date(2000,03,10)
#start = date(1997,8,5)
#end = date(1997,5,23)

delta = end - start         # timedelta

#create an array full of the date buckets
for i in range(delta.days + 1):
	days.append(str(start + timedelta(days=i)))
	datetimes.append(datetime.datetime.strptime(days[i], '%Y-%m-%d'))
	val.append(float(0.0))
	counts.append(0)

ifile = open('example.csv',"rU")
reader = csv.reader(ifile)
rownum=0
#fill the array buckets (aka create histogram values) 
datesMissing = []
for row in reader:
	if str(row[0]) in days:
		dateIndex = days.index(str(row[0]))
		if row[1]:
			#aggregate the stocks AND track the number of stocks per date. Can be used later to compute the average
			val[dateIndex]+=float(row[1])
			counts[dateIndex]+=1

#write bucketed data to a csv
with open('dotComHistoData.csv','wb') as outfile:
	iterator = 0
	spamwriter = csv.writer(outfile, lineterminator='\n')
	for row in val:
		spamwriter.writerow([datetimes[iterator],val[iterator],counts[iterator]])
		iterator+=1
averagesData = takeAverage(val,counts)
plt.plot(datetimes,averagesData)
plt.show()


ifile.close()
