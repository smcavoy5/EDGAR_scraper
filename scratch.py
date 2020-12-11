import requests
import re

#enter the year with 
year = input("Enter the year: ")

while len(year) != 4 or int(year) < 1990:
	print("Input must be of the form XXXX (ex: 2013)"   
		+ " and must be after the year ...")
	year = input("Enter the year: ")

quarter = input("Enter the quarter: ")

while len(quarter) != 1 or int(quarter) > 4 or int(quarter) < 1:
	print("Input must be of the form X (ex: 3 for the third quarter)"   
		+ " and must between 1 and 4")
	quarter = input("Enter the quarter: ")

quarter = 'QTR' + quarter


tickers = {}

with open('tickers.txt') as f:
	for line in f:
		obj = line.split('\t')
		tickers[obj[0]] = obj[1][:-1]


# given a ticker return the unique CIK 
def getCIK(ticker):
	"""PRE: needs to be in tickers"""
	return tickers[ticker.lower()]

# use the master index with a certain year and quarter
r = requests.get("https://www.sec.gov/Archives/edgar/full-index/{}/{}/master.idx".format(year, quarter))



#testing code
cik = getCIK('aapl')
tenQ = '10-Q'
tenK = '10-K'

# The format is:
# CIK|Company Name|Form Type|Date Filed|Filename
# the '\|' finds the instance of '|' 
# the [^|]* finds all the characters before the instance of '|'
# we are only looking at the 10-K or 10-Q right now
pattern = cik + '\|[^|]*\|' + '((10\-K)|(10\-Q))' + '\|[^|]*\|[^.]*'
line = re.search(pattern, r.text)

# FORMAT: [CIK, COMPANY NAME, FORM TYPE, DATE FILED, FILENAME]
company_information = line.group().split('|')

filename = company_information[4]
form = filename + ".txt"
r = requests.get("https://www.sec.gov/Archives/" + form)
print(r.text[:1000])














