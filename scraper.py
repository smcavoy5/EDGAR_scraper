import requests
import re


# Create a dictionary that matches a companies ticker (ex: 'aapl')
# with their unique CIK. TYhis is done so if we are given a ticker
# we can find the correct 10-K using the CIK number
tickers = {}
with open('tickers.txt') as f:
	for line in f:
		obj = line.split('\t')
		tickers[obj[0]] = obj[1][:-1]

# The filings in EDGAR are avaible from 1994Q3 onward
# so when taking input for the year, quarter, and ticker
# manual checks can be coded in to stop errors when accessing
# a wrong date or ticker
# get the year (ex: 2009), the quarter (ex: 3), and the ticker (ex: appl)
year = input("Enter the year: ")
quarter = 'QTR' + input("Enter the quarter: QTR")
ticker = input("Enter the ticker: ")

# given a ticker return the unique CIK 
# this function isn't really neccessary as of now
def getCIK(ticker):
	"""PRE: needs to be in tickers"""
	return tickers[ticker.lower()]


# use the master index with a given year and quarter
r = requests.get("https://www.sec.gov/Archives/edgar/full-index/{}/{}/master.idx".format(year, quarter))

# get the unique CIK associated with the company
cik = getCIK(ticker)


# The format for each report is:
# CIK|Company Name|Form Type|Date Filed|Filename
# the '\|' finds the instance of '|' 
# the [^|]* finds all the characters before the instance of '|'
pattern = cik + '\|[^|]*\|' + '((10\-K)|(10\-Q))' + '\|[^|]*\|[^.]*'
line = re.search(pattern, r.text)

# we should now have the entire line that contains the companies
# CIK, name, form type, date filed, and the file name with that will allow 
# us to access the 10-K/10-Q
# NOTE: The above code can be modified to find any form

# FORMAT: [CIK, COMPANY NAME, FORM TYPE, DATE FILED, FILENAME]
# store the information for access letter
company_information = line.group().split('|')

# Now we actually grab the txt file which is the 10-K/10-Q
# which can be parsed for more information
form = company_information[4] + ".txt"
report = requests.get("https://www.sec.gov/Archives/" + form)


#raw report is the 10-K/10-Q form
raw_report = report.text
