# CryptoBubbleAnalysis

This repository includes all the code I used to analytically compare the cryptocurrency bubble and the dotcom bubble. Below is an overview of each file: 

main.py: this is where most of the analysis was conducted. 

analysisFunctions.py: this is where I wrote most of the functions used to analyze the data

companylist.csv: this is the list of companies whose stock prices I used to represent the dotcom bubble

financeDataReader.py: this is where I scraped all the raw finance data on the 600 companies (using their tickers)

financeDataCleaner.py: this is where I took all the raw stock price data, isolated the closing prices, and summing them by date (effectively creating buckets, similar to histogram data) for use later on in the main.py file

bitcoinPriceScraper.py: this is the code I used to query the bitcoin prices