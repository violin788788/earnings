#import sys
from sec_edgar_downloader import Downloader
dl = Downloader("YourCompanyName", "your@email.com")

stock = "msft"

stock = stock.upper()
print(stock)

print(stock+" getting quarterly reports")
# Quarterly reports (10-Q)
dl.get("10-Q", stock, after="2022-01-01", before="2025-01-01")
print(stock+" getting yearly reports")
# Annual reports (10-K)
dl.get("10-K", stock, after="2022-01-01", before="2025-01-01")
