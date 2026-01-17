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



#char_1000(stocks)
def char_1000(stocks):
    for stock in stocks:
        stock_file = os.path.join("sec-edgar-filings",stock)
        try:
            times_of_year = os.listdir(stock_file)
        except:
            print(stock,"no values for it")
            continue
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
            print("have to wait",wait_time,"seconds",a+1)





#get_sec_earn_dates(stocks)
def get_sec_earn_dates(stocks):
    from sec_edgar_downloader import Downloader
    dl = Downloader("YourCompanyName", "your@email.com")    
    for a, stock in enumerate(stocks):
        if "Symbol" in stock:
            continue
        check = os.path.join("sec-edgar-filings",stock)
        if os.path.exists(check):
            continue
        print(a,stock,"getting quarterly reports")
        # Quarterly reports (10-Q)
        dl.get("10-Q", stock, after="2022-01-01", before="2025-01-01")
        try:
            char_1000([stock])
        except:
            meow = "meow"
        print(a,stock,"getting yearly reports")
        # Annual reports (10-K)
        dl.get("10-K", stock, after="2022-01-01", before="2025-01-01")
        try:
            char_1000([stock])
        except:
            continue

#stocks = get_stock_list(csv_file)
def get_stock_list(csv_file):
    import csv
    back = []
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            stock = row[0]
            if "Symbol" in stock:
                continue
            print(stock,row)
            back.append(stock)
    return back

import os
stocks = get_stock_list("500.csv")
for a,stock in enumerate(stocks):
    print(a,stock)
#get_sec_earn_dates(stocks)
#char_1000(stocks)
price_history(stocks)
#mine_earn_dates(stocks):
#gen_analysis(stocks)


