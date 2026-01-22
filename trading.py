didnt_work=[

            #"TSM","BRK.A","C","MS","SO","DUK","BLK",
            #"ANTM","MET"
]
#,"BRKA","ANTM"

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
            print("price history already exists",stock)
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


#gap_to_procent(price_before,price_after)
def gap_to_procent(price_before,price_after):
    gap = float(price_after/price_before)
    gap = (gap-1)*100
    gap = (int(gap*100))/100
    return(gap)

#gap = convert_to_procent(gap)
def convert_to_procent(value):
    value = value-1
    value = int(value*10000)
    value = float(value/100)
    return value

#history = load_history(stock)
def load_history(file):
    import csv
    history_file = os.path.join("price_history",stock+"_polygon_daily.csv")
    history_headers = []
    #print(history_file)
    first_row = "not_initiated"
    history = {}
    header = []
    with open(history_file, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if first_row=='not_initiated':
                for b,val in enumerate(row):
                    header.append(val)
                first_row = 'initiated'
                continue
            new_info = {}
            for b,val in enumerate(header):
                #if b==0:
                #    continue
                new_info[val] = row[b]
            history[row[0]] = new_info
    return history




def gen_trend(stocks,earnings_folder):
    from datetime import datetime, time,timedelta
    back = []
    same_most_index = []
    master = {}
    old_stock="--initiate--"
    for a,stock in enumerate(stocks):
        if "Symbol" in stock:
            continue
        history = load_history(stock)
        earn_dates = {}
        stock_folder = os.path.join(earnings_folder,stock)
        #print(stock_folder)
        try:
            list_stock_folder = os.listdir(stock_folder)
        except:
            continue
        earnings_info = {}
        locations = []
        counter = 0
        stock_earnings = {}
        stock_info = {}
        aggregate = {}
        earn_list = {}
        for b,folder_time in enumerate(list_stock_folder):
            earn_list[folder_time] = {}
            randoms = os.listdir(os.path.join(earnings_folder,stock,folder_time))
            for c,random in enumerate(randoms):
                info = {}
                specific = os.path.join(earnings_folder,stock,folder_time,random,"full-submission.txt")
                #print("specific",specific)
                counter = counter+1
                with open(specific, "r", encoding="utf-8") as f:
                    content = f.read()
                iden = "<ACCEPTANCE-DATETIME>"
                begin = content.find(iden)
                end = content.find("\n",begin)
                acceptance_timestamp = content[begin:end]
                begin_iden = ">"
                begin_location = acceptance_timestamp.find(begin_iden)+len(begin_iden)
                end_location = len(acceptance_timestamp)
                extracted = acceptance_timestamp[begin_location:end_location]
                converted =extracted[0:4]+"-"+extracted[4:6]+"-"+extracted[6:8]+" "+extracted[8:10]+":"+extracted[10:12]+":"+extracted[12:14]
                str_date = converted[0:converted.find(" ")]
                object_release = datetime.strptime(converted, "%Y-%m-%d %H:%M:%S")
                object_date = datetime.strptime(str_date, "%Y-%m-%d")
                time_of_release = object_release.time()#time_of_release = time_of_release.time()
                str_time_of_release = time_of_release.strftime("%H:%M:%S")
                before_market_open = "BMO"
                after_market_close = "AMC"
                during_market = "during market?"
                if time_of_release >= time(16, 0):
                    BMO_or_AMC = after_market_close
                    session_before = object_date
                    session_after = object_date + timedelta(days=1)
                elif time_of_release  < time(9, 30):
                    BMO_or_AMC = before_market_open
                    session_before = object_date - timedelta(days=1)
                    session_after = object_date
                else:
                    BMO_or_AMC = during_market
                    session_before = during_market
                    session_after = during_market
                try:
                    session_before = session_before.strftime("%Y-%m-%d")
                    session_after = session_after.strftime("%Y-%m-%d")
                except:
                    continue
                    skip = "skip"




                if stock!=old_stock:
                    master[stock] = {}
                    old_stock = stock

                new = {}
                new["acceptance_timestamp"]=acceptance_timestamp
                new["extracted"]=extracted
                new["converted"]=converted
                new["str_time_of_release"]=str_time_of_release
                new["BMO_or_AMC"]=BMO_or_AMC
                new["session_before"]=session_before
                new["session_after"]=session_after
                new["folder_time"] = folder_time
                new["random"] = random
                master[stock][str_date]=new
                price_info_day_before = ""
                price_info_day_after = ""
                found_begin = 0
                found_after = 0
                for date,price_info in history.items():
                    if session_before in date:
                        new["prices_before"] = price_info
                        found_begin = 1
                        #print("prices_before",price_info)
                    if session_after in date:
                        new["prices_after"] = price_info
                        found_after = 1
                        #print("prices_after",price_info)
                not_found = "-----not found===--"
                if found_begin==0:
                    new["prices_before"] = not_found
                if found_after==0:
                    new["prices_after"] = not_found
                    """
                print("")
                print('new["prices_before"]',new["prices_before"])
                print('new["prices_after"]',new["prices_after"])
                """
                if not_found not in new['prices_after']:
                    print(new['prices_after']['open'])

                
                if not_found==new["prices_before"] or not_found==new["prices_after"]:
                    continue
                
                #print('new["prices_after"]["open"]',new["prices_after"]["open"])

                new['gap'] = float(new["prices_after"]["open"])/float(new["prices_before"]["close"])
                new['move_up'] = float(new["prices_after"]["high"])/float(new["prices_after"]["open"])
                new['move_down'] = float(new["prices_after"]["low"])/float(new["prices_after"]["open"])
                new['move_close'] = float(new["prices_after"]["close"])/float(new["prices_after"]["open"])

                new['gap'] = convert_to_procent(new['gap'])
                new['move_up'] = convert_to_procent( new['move_up'])
                new['move_down'] = convert_to_procent(new['move_down'])
                new['move_close'] =convert_to_procent(new['move_close'])
  
                continue

                try:
                    close_day_before = float(info["before_info"]["close"])
                    price_open = float(info["after_info"]["open"])
                    price_high = float(info["after_info"]["high"])
                    price_low = float(info["after_info"]["low"])
                    close_dayof = float(info["after_info"]["close"])
                    gap = gap_to_procent(close_day_before,price_open)
                    move_up = gap_to_procent(price_open,price_high)
                    move_down = gap_to_procent(price_open,price_low)
                    move_close = gap_to_procent(price_open,close_dayof)
                    vp_before = int(float(info["before_info"]["volume"])*float(info["before_info"]["close"]))
                    vp_after = int(float(info["after_info"]["volume"])*float(info["after_info"]["open"]))
                    #if vp_after<vp_before:
                    #    continue

                    info["vp_before"] = vp_before
                    info["vp_after"] = vp_after

                    info["gap"] = {"gap":gap,"price_open":price_open,"close_day_before":close_day_before}
                    info["move_up"] = {"move_up":move_up,"price_high":price_high,"price_open":price_open}
                    info["move_down"] = {"move_down":move_down,"price_low":price_low,"price_open":price_open}
                    info["move_close"] = {"move_close":move_close,"close_dayof":close_dayof,"price_open":price_open}
                    #info["moves"]=moves
                    #except:
                    #    continue
                    earnings_info[str_date] = info
                except:
                    continue

    file_name = "earnings"
    out_json =file_name+".json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(master, f, indent=4)
    out_html = file_name+".html"
    with open(out_html, "w", encoding="utf-8") as f:
        f.write("<pre>")
        f.write(json.dumps(master, indent=4))
        f.write("</pre>")
    os_name = platform.system()
    if "Linux" in os_name:
        copied_to_templates = "/home/info34/mysite/templates/"+file_name+".html"
    if "Windows" in os_name:
        #copied_to_templates = "/home/info34/mysite/templates/"+file_name+".html"
        copied_to_templates = r"A:\Users\-\0code\info34\mysite\templates\\"+file_name+".html"
    shutil.copy(out_html, copied_to_templates)
    #"/mysite/templates/earnings.html"
    #/home/info34/mysite/templates39% full – 199.6 MB of your 512.0 MB quota More Info Open Ba
    os_name = platform.system()
    if "Windows" in os_name:
        os.startfile(out_json)
        os.startfile(copied_to_templates)

#--------run stuff--------------------------------------------------------------------#
import os,sys,json,platform,shutil
stocks = get_stock_list("500.csv")

how_many_stocks = 250

stocks = stocks[0:how_many_stocks]
for a,stock in enumerate(stocks):
    print(a,stock)
#get_sec_earn_dates(stocks)
#sec_1000_chars(stocks)
#price_history(stocks)
gen_trend(stocks,"sec-edgar-filings")


