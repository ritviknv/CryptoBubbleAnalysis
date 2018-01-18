import urllib, json
import requests
import csv
from datetime import date, timedelta
import datetime
import calendar


datesArray = []
days = []
pricesArray = []

start = date(2013,9,01)
end = date(2017,9,05)

delta = end - start         # timedelta

#create an array full of the date buckets
for i in range(delta.days + 1):
	days.append(str(start + timedelta(days=i)))
	datesArray.append(datetime.datetime.strptime(days[i], '%Y-%m-%d'))

r = requests.get('https://api.coindesk.com/v1/bpi/historical/close.json?start=2013-09-01&end=2017-09-05')
pricesMap = (r.json())['bpi']
index = 0
for i in days:
	pricesArray.append(pricesMap[i])

with open('cryptoprices.csv', 'wb') as outfile: 
	iterator = 0
	spamwriter = csv.writer(outfile, lineterminator='\n')
	for row in pricesArray:
		spamwriter.writerow([datesArray[iterator],pricesArray[iterator],"BTC"])
		iterator+=1