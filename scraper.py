import requests
import re

# Create a dictionary for the tickers and CIK
tickers = {}
with open('tickers.txt') as f:
	for line in f:
		obj = line.split('\t')
		tickers[obj[0]] = obj[1][:-1]


# get the year (ex: 2009), the quarter (ex: 3), and the ticker (ex: appl)
year = input("Enter the year: ")
quarter = 'QTR' + input("Enter the quarter: QTR")
ticker = input("Enter the ticker: ")

# given a ticker return the unique CIK 
def getCIK(ticker):
	"""PRE: needs to be in tickers"""
	return tickers[ticker.lower()]

# use the master index with a certain year and quarter
r = requests.get("https://www.sec.gov/Archives/edgar/full-index/{}/{}/master.idx".format(year, quarter))


#testing code
cik = getCIK(ticker)


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

#r is the 10-K/10-Q form
