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



#sec_1000_chars(stocks)
def sec_1000_chars(stocks):
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
                if len(content)==1000:
                    print(stock,random,"already 1000 chars")
                    continue
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
    for a,stock in enumerate(stocks):
        out_name = stock+"_polygon_daily.csv"
        OUT_FILE = os.path.join(folder_history,out_name)
        if out_name in list_history:
            print("price history alrexists",stock)
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
        print(a,stock,"Saved to",OUT_FILE,"rows:",len(df))
        wait_time = 15
        for a in range(0,wait_time):
            time.sleep(1)
            print("have to wait",wait_time,"seconds",a+1)





#get_sec_earn_dates(stocks)
def get_sec_earn_dates(stocks):
    from sec_edgar_downloader import Downloader
    dl = Downloader("YourCompanyName", "your@email.com")
    begin_date = "2023-01-01"    
    end_date = "2026-01-01"    
    for a, stock in enumerate(stocks):
        if "Symbol" in stock:
            continue
        check = os.path.join("sec-edgar-filings",stock)
        if os.path.exists(check):
            continue
        print(a,stock,"getting quarterly reports")
        # Quarterly reports (10-Q)
        dl.get("10-Q", stock, after=begin_date, before=end_date)
        try:
            sec_1000_chars([stock])
        except:
            meow = "meow"
        print(a,stock,"getting yearly reports")
        # Annual reports (10-K)
        dl.get("10-K", stock, after=begin_date, before=end_date)
        try:
            sec_1000_chars([stock])
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

def gen_check():
    out_text = ""
    folders = ["sec-edgar-filings","price_history"]
    for a,folder in enumerate(folders):
        list_dir = os.listdir(folder)
        number = len(list_dir)
        out_str = str(number)+"_"+str(folder)
        out_file = out_str+".txt"
        print(out_str)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(out_file)



#def earnings_find(folder):
#gen_trend(stocks,"sec-edgar-filings"):
def gen_trend(stocks,earnings_folder):
    import csv
    back = []
    for a,stock in enumerate(stocks):
        if "Symbol" in stock:
            continue
        earn_dates = []
        folder_stock = os.path.join(earnings_folder,stock)
        try:
            times_of_year = os.listdir(folder_stock)
        except:
            continue
        for b,time_of_year in enumerate(times_of_year):
            folder_time_of_year = os.path.join(folder_stock,time_of_year)
            randoms = os.listdir(folder_time_of_year)
            for c,random in enumerate(randoms):
                folder_random = os.path.join(folder_time_of_year,random)
                specific_file = os.path.join(folder_random,"full-submission.txt")
                with open(specific_file, "r", encoding="utf-8") as f:
                    content = f.read()
                iden = "FILED AS OF DATE:"
                begin = content.find(iden)
                end = content.find("\n",begin)
                earn_date = content[begin:end]
                correct_format = earn_date.replace(iden,"")
                correct_format = correct_format.replace("\t","")
                correct_format = correct_format[:4] + "-" + correct_format[4:6] + "-" + correct_format[6:]
                earn_dates.append(correct_format)
        earn_dates.sort()
        print(a,stock)
        for b,date in enumerate(earn_dates):
            print(date)
        history_file = os.path.join("price_history",stock+"_polygon_daily.csv")
        prices = []
        with open(history_file, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if "Symbol" in stock:
                    continue
                prices.append(row)
        #print("prices",prices)
        #print(earn_dates)
        #date,volume,vw,open,close,high,low,t,n
        last_2_years = []
        matches = 0
        for b,earn_date in enumerate(earn_dates):
            three_days = []
            for c,price in enumerate(prices):
                price_date = price[0]
                if earn_date in price_date:
                    matches+=1
                    """
                    last_2_years.append(prices[c-1])
                    last_2_years.append(price)
                    last_2_years.append(prices[c+1])
                    """
                    three_days.append(prices[c-1])
                    three_days.append(price)
                    three_days.append(prices[c+1])
                    last_2_years.append(three_days)
                    print("three_days",three_days)
                    break
        for b,three_days in enumerate(last_2_years):
            print(stock)
            most = 0
            last_vp = -1
            for c,day_info in enumerate(three_days):
                old_date = day_info[0]
                new_date = old_date[0:old_date.find(" ")]
                day_info[0] = new_date
                vol = float(day_info[1])
                cost = float(day_info[3])
                vp = int(vol*cost)
                day_info = [vp]+day_info
              # day_info[0] = day_info[0][0:day_info.find(" ")]
                print("date",day_info)

        sys.exit()

        for b,three_days in enumerate(last_2_years):
            for c,day in enumerate(three_days):
                vol = day[1]
                start = day[3]
                if "volume" in vol:
                    continue
                vp = int(float(vol)*float(start))
                last_2_years[b][c] = [vp]+day

        for b,three_days in enumerate(last_2_years):
            check_vp = []
            for c,day in enumerate(three_days):
                #check_vp.append(day[])
                print("day",day)

    



       


     
        """
    for folder_name in stocks:
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
 





import os,sys
stocks = get_stock_list("50.csv")
for a,stock in enumerate(stocks):
    print(a,stock)
get_sec_earn_dates(stocks)
sec_1000_chars(stocks)
price_history(stocks)
#mine_earn_dates(stocks)
gen_trend(stocks,"sec-edgar-filings")
#gen_check()



"""
        person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}       
"""


