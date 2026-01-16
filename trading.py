didnt_work=[

            #"TSM","BRK.A","C","MS","SO","DUK","BLK",
            #"ANTM","MET"
]
#,"BRKA","ANTM"


top_100 = [
    "TSM","C","MS","SO","DUK","BLK",
    "MET",

    "NVDA", "AAPL", "GOOGL", "MSFT", "AMZN",
    "AVGO", "META","TSLA",
    "LLY", "WMT", "JPM", "V", "JNJ",
    "XOM", "UNH", "BAC", "MA", "NVDA",  # NVDA appears high and repeated for emphasis
    "ORCL", "VZ", "HD", "PEP", "KO",
    "PG", "COST", "CRM", "ADBE", "CSCO",
    "TMO", "CVX", "ABBV", "ACN", "NKE",
    "MDT", "AVY", "UPS", "SCHW",
    "TMUS", "DHR", "TXN", "LOW",
    "NEE", "RTX", "HON", "COP", "IBM",
    "QCOM", "INTU", "AMGN", "SBUX", "GE",
    "PLD", "AXP", "CME", "BKNG", "MMM",
    "SPGI", "CI",
    "CCI", "ISRG", "GILD", "BSX",
    "FISV", "KMB", "CL", "ETN",
    "ZTS", "ADP", "AON", "PGR",
    "EL", "TJX", "CB", "FITB", "KEY",
    "HBAN", "MCO", "HUM", "ICE", "ALL",
    "PSA", "KMI", "CNC", "RSG", "ETR",
    "PEG", "XEL", "AWK", "ECL", "KR",
    "DG", "HLT", "D", "EOG", "OXY",
    "MPC", "CVS"
]


def char_1000(stock):
    stock_file = os.path.join("sec-edgar-filings",stock)
    folder_yearly = os.path.join(stock_file,"10-K")
    folder_quarterly = os.path.join(stock_file,"10-Q")
    print(folder_yearly)
    print(folder_quarterly)
    files_yearly = os.listdir(folder_yearly)
    files_quarterly = os.listdir(folder_quarterly)
    print(files_yearly)
    print(files_quarterly)
    # Truncate yearly reports
    for folder_name in files_yearly:
        print(folder_name)
        file_path = os.path.join(folder_yearly, folder_name,"full-submission.txt")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content[:1000]  # keep only first 1000 chars
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Truncated yearly report: {folder_name}")
    for folder_name in files_quarterly:
        print(folder_name)
        file_path = os.path.join(folder_quarterly, folder_name,"full-submission.txt")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content[:1000]  # keep only first 1000 chars
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Truncated quarterly report: {folder_name}")


def earn_dates(folder):
    files = os.listdir(folder)
    back = []
    for folder_name in files:
        #print(folder_name)
        file_path = os.path.join(folder, folder_name,"full-submission.txt")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        iden = "FILED AS OF DATE:"
        begin = content.find(iden)
        end = content.find("\n",begin)
        earn_date = content[begin:end]
        #print(earn_date)
        #print(type(earn_date))
        #earn33 = earn_date[earn_date.find("\t"):len(earn_date)]
        #earn33 = earn33.replace("\t","")
        #print(earn33)
        #back.append(earn33)
        back.append(earn_date)
    return back

def mine_dates(stock):
    stock_file = os.path.join("sec-edgar-filings",stock)
    folder_yearly = os.path.join(stock_file,"10-K")
    folder_quarterly = os.path.join(stock_file,"10-Q")
    print(folder_yearly)
    print(folder_quarterly)
    files_yearly = os.listdir(folder_yearly)
    files_quarterly = os.listdir(folder_quarterly)
    print(files_yearly)
    print(files_quarterly)
    # Truncate yearly reports
    reports_yearly = earn_dates(folder_yearly)
    reports_quarterly = earn_dates(folder_quarterly)
    reports = reports_yearly+reports_quarterly
    reports.sort()
    for date in reports:
        print(date)





from pathlib import Path
import sys,os
from sec_edgar_downloader import Downloader
dl = Downloader("YourCompanyName", "your@email.com")
stock = "aapl"
stock = stock.upper()
stocks = [stock]
print(stock)
cwd = os.getcwd()
print (cwd)

#mine_dates(stock)
#char_1000(stock)

#sys.exit()
#function   sec vs fix
function = "sec"
stocks = top_100
for a, stock in enumerate(top_100):
    print(a, stock)
    if function=="fix":
        try:
            #char_1000(stock)
            mine_dates(stock)
        except:
            continue
        continue

    check = os.path.join("sec-edgar-filings",stock)
    if os.path.exists(check):
        continue
    #mine_dates(stock)
    #continue
    print(stock)
    print(stock+" getting quarterly reports")
    # Quarterly reports (10-Q)
    dl.get("10-Q", stock, after="2022-01-01", before="2025-01-01")
    try:
        char_1000(stock)
    except:
        meow = "meow"
    print(stock+" getting yearly reports")
    # Annual reports (10-K)
    dl.get("10-K", stock, after="2022-01-01", before="2025-01-01")
    try:
        char_1000(stock)
    except:
        continue