didnt_work=[

            #"TSM","BRK.A","C","MS","SO","DUK","BLK",
            #"ANTM","MET"
]
#,"BRKA","ANTM"


top_100 = [
    "C","MS","SO","DUK","BLK",
    "MET","TSM",

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

def earnings_find(folder):
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




    """
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
        """



def mine_dates(stock):
    stock_file = os.path.join("sec-edgar-filings",stock)
    folder_yearly = os.path.join(stock_file,"10-K")
    folder_quarterly = os.path.join(stock_file,"10-Q")
    print(folder_yearly)
    print(folder_quarterly)
    # Truncate yearly reports
    reports_yearly = earnings_find(folder_yearly)
    reports_quarterly = earnings_find(folder_quarterly)
    reports = reports_yearly+reports_quarterly
    reports.sort()
    for date in reports:
        print(date)
    return reports




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


#function = sec,mine,gen_report,yahoo
function = "gen_report"
#gen..what kind of file to have data?
stocks = top_100
output = []


#char_1000(stocks)
def char_1000(stocks):
    for stock in stocks:
        stock_file = os.path.join("sec-edgar-filings",stock)
        times_of_year = os.listdir(stock_file)
        print(times_of_year)
        for time_of_year in times_of_year:
            dir_random = os.path.join(stock_file,time_of_year)
            randoms = os.listdir(dir_random)
            for random in randoms:
                specific_file = os.path.join(dir_random,random,"full-submission.txt")
                with open(specific_file, "r", encoding="utf-8") as f:
                    content = f.read()
                content = content[:1000]  # keep only first 1000 chars
                with open(specific_file, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Truncated yearly report: {specific_file}")


def price_history(stocks):
    import time
    import requests
    import pandas as pd
    API_KEY="65JaxrhDSYET1StvPxZy1KgpnttWna98"
    folder_history = "price_history"
    list_history = os.listdir(folder_history)
    for stock in stocks:
        out_name = stock+"_polygon_daily.csv"
        OUT_FILE = os.path.join(folder_history,out_name)
        if out_name in list_history:
            print("skip",stock)
            continue
        #SYMBOL="AAPL"
        FROM_DATE="2023-01-01"
        TO_DATE="2026-01-01"
        OUT_FILE = os.path.join(folder_history,stock+"_polygon_daily.csv")
        #OUT_FILE="price_history//"+stock+"_polygon_daily.csv"
        BASE_URL=f"https://api.polygon.io/v2/aggs/ticker/{stock}/range/1/day/{FROM_DATE}/{TO_DATE}"
        params={"adjusted":"true","sort":"asc","limit":50000,"apiKey":API_KEY}
        all_bars=[]
        url=BASE_URL
        while url:
            print(f"Fetching: {url}")
            r=requests.get(url,params=params)
            if r.status_code==429:
                print("Rate limit hit, sleeping 60s")
                time.sleep(60)
                continue
            r.raise_for_status()
            data=r.json()
            if "results" in data:
                all_bars.extend(data["results"])
            url=data.get("next_url")
            if url:
                url+=f"&apiKey={API_KEY}"
                time.sleep(15)
        df=pd.DataFrame(all_bars)
        df["date"]=pd.to_datetime(df["t"],unit="ms")
        df.set_index("date",inplace=True)
        df.rename(columns={"o":"open","h":"high","l":"low","c":"close","v":"volume"},inplace=True)
        df.to_csv(OUT_FILE)
        print(df.head())
        print("Saved to",OUT_FILE,"rows:",len(df))
        wait_time = 15
        for a in range(0,wait_time):
            time.sleep(1)
            print("waiting to not go over limit",a+1,wait_time)




#---------------main function-------------------



for a, stock in enumerate(top_100):
    print(a, stock)
    if function=="gen_report":
        try:
            #char_1000(stock)
            reports = mine_dates(stock)
            print("reports",reports)
            new_dates = []
            for date in reports:
                new = date.replace("FILED AS OF DATE:\t\t","")
                #print(new)
                new_dates.append(new)
            new_dates.sort()
            to_out = [stock,new_dates]
            print(stock,new_dates)
            output.append(to_out)
        except:
            continue
        continue
    check = os.path.join("sec-edgar-filings",stock)
    if os.path.exists(check):
        continue
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
#print(output)
output.sort()
out_text = ""
for item in output:
    print(item)
    out_text=out_text+str(item)+"\n"
out_file ='earn_dates.txt'
with open(out_file, 'w') as file:
    # Write text to the file
    file.write(out_text)
os.startfile(out_file)






#get_sec_dates(stocks):
#char_1000(stocks)
#gen_reports(stocks):
price_history(stocks)
