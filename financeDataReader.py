import pandas_datareader.data as data
import csv
import datetime

symbolList = []
ifile = open('companylist.csv',"rb")
reader = csv.reader(ifile)
rownum=0
#make an array full of the tickers of interest
for row in reader:
	if rownum==0:
		print("header")
	else:
		if row[5]!='2017':
			sampleTemp = row[0]
			sampleTemp.replace(" ","")
			symbolList.append(sampleTemp)
	rownum+=1

ifile.close()


symbolTest = 'AMZN'
data_source='yahoo'
start_date = '1980-01-01'
end_date = '2017-10-01'

start = datetime.datetime(1980,1,1)
end = datetime.datetime(2017,10,10)

df = data.DataReader(symbolTest,'yahoo',start,end)
df.to_csv('testOutput.csv')


# dfMaster = data.DataReader(symbolTest,'yahoo',start,end)
# for x in range(0,len(dfMaster)):
# 		symbolList2.append(symbolTest)
# dfMaster['Symbol'] = symbolList2
# symbolList2 = []
# print(dfMaster)
#dfMaster = data.DataReader(symbolList,'yahoo',start,end)
#for a given symbol, pull a data reader
# for symbol in symbolList:
# 	df = data.DataReader(symbol,'yahoo',start,end)
# 	print(df.to_string())
# 	#add the tickername to the last column of the dataframe
# 	for x in range(0,len(df)):
# 		symbolList2.append(symbol)
# 	df['Symbol'] = symbolList2
# 	symbolList2 = []
# 	dfMaster = dfMaster.append(df)
# dfMaster.to_csv('example2.csv')
