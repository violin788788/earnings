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


#gap_to_procent(close_price,open_price)
def gap_to_procent(before_price,after_price):
    gap = float(after_price/before_price)
    gap = (gap-1)*100
    gap = (int(gap*100))/100
    return(gap)

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
                if b==0:
                    continue
                new_info[val] = row[b]
            history[row[0]] = new_info
    return history




#def earnings_find(folder):
#gen_trend(stocks,"sec-edgar-filings"):
def gen_trend(stocks,earnings_folder):
    #from datetime import datetime, timedelta
    #from datetime import datetime
    from datetime import datetime, time,timedelta
    #from datetime import time
    back = []
    same_most_index = []
    master = {}
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
        info = {}
        
        locations = []
        counter = 0
        for b,folder_time in enumerate(list_stock_folder):
            randoms = os.listdir(os.path.join(earnings_folder,stock,folder_time))
            for c,random in enumerate(randoms):
                specific = os.path.join(earnings_folder,stock,folder_time,random,"full-submission.txt")
                #print("specific",specific)
                counter = counter+1
                info["file"] = specific
                with open(specific, "r", encoding="utf-8") as f:
                    content = f.read()
                iden = "<ACCEPTANCE-DATETIME>"
                begin = content.find(iden)
                end = content.find("\n",begin)
                acceptance_timestamp = content[begin:end]
                info["acceptance_timestamp"] = acceptance_timestamp
                begin_iden = ">"
                begin_location = acceptance_timestamp.find(begin_iden)+len(begin_iden)
                end_location = len(acceptance_timestamp)
                extracted = acceptance_timestamp[begin_location:end_location]
                info["extracted"] = extracted
                converted =extracted[0:4]+"-"+extracted[4:6]+"-"+extracted[6:8]+" "+extracted[8:10]+":"+extracted[10:12]+":"+extracted[12:14]
                info["converted"] = converted
                info["date"] = converted[0:converted.find(" ")]
                info["time"] = converted[converted.find(" ")+1:len(converted)]
                #date_object = datetime.strptime(info["date"], "%Y-%m-%d")
                #time_object = datetime.strptime(info["time"], "%H:%M:%S")
                object_release = datetime.strptime(converted, "%Y-%m-%d %H:%M:%S")
                object_date = datetime.strptime(info["date"], "%Y-%m-%d")
                time_of_release = object_release.time()#time_of_release = time_of_release.time()  
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
                    skip = "skip"
                info["session_before"] = session_before
                info["session_after"] = session_after
             


        for key,val in info.items():
            print(key,"=",val)
        print("")
        continue
        #master[stock]=info


        last_2_years = {}
        count = 0
        for b,sec_datetime in enumerate(earn_dates):
            from datetime import datetime, timedelta
            dates_to_gather = []
            date_of_release = timestamp_release.date()
            dates_to_gather = []
            if BMO_or_AMC == after_market_close:
                dates_to_gather.append(date_of_release)
                dates_to_gather.append(date_of_release + timedelta(days=1))
            elif BMO_or_AMC == before_market_open:
                dates_to_gather.append(date_of_release - timedelta(days=1))
                dates_to_gather.append(date_of_release)
            else:
                dates_to_gather.append(during_market)
                dates_to_gather.append(during_market)
            count = count+1
            days_2 = {}
            days_2["sec_datetime"]=sec_datetime
            days_2["sec_numbers"]=sec_numbers
            days_2["timestamp_release"]=timestamp_release
            days_2["timestamp_str"]=timestamp_str
            days_2["time_of_release"]=time_of_release    
            days_2["BMO_or_AMC"]=BMO_or_AMC
            days_2["session_before"]=str(dates_to_gather[0])
            days_2["session_after"]=str(dates_to_gather[1])  
            #last_2_years.append(days_2)
            last_2_years[stock+"-"+timestamp_str]=days_2
        history_file = os.path.join("price_history",stock+"_polygon_daily.csv")
        array_prices = []
        with open(history_file, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if "Symbol" in stock:
                    continue
                array_prices.append(row)
        heading_order = []
        heading_order.append("date")
        heading_order.append("volume")
        heading_order.append("volume_weighted_price")
        heading_order.append("open")
        heading_order.append("high")
        heading_order.append("low")
        heading_order.append("close")
        count = 0
        price_history = {}
        for b,day_info in enumerate(array_prices):
            increase = -1
            conversion = {}
            for c,header in enumerate(heading_order):
                increase=increase+1
                conversion[header] = day_info[increase]
            price_history[day_info[0]]=conversion
        for release_date, earnings_info in last_2_years.items():
            session_before = last_2_years[release_date]["session_before"]
            session_after = last_2_years[release_date]["session_after"]
            for price_date, day_info in price_history.items():
                volume = day_info["volume"]
                open_price = day_info["open"]
                if "volume" in volume:
                    continue
                vol_pri = int(float(volume)*float(open_price))
                new = {}
                if session_before in price_date:
                    new["vol_pri"] = vol_pri
                    for info,day_info in day_info.items():
                        new[info] = day_info
                    last_2_years[release_date]["before_data"] = new
                if session_after in price_date:
                    new["vol_pri"] = vol_pri
                    for info,day_info in day_info.items():
                        new[info] = day_info
                    last_2_years[release_date]["after_data"] = new
        #gaps = {}
        #gaps = []
        #moves_up = []
        #moves_down = []
        #moves = []
        for release_date, earnings_info in last_2_years.items():
            #print (release_date,earnings_info)
            for title,info in earnings_info.items():
                print(title,info)
            continue 
            try:
                close_day_before = float(earnings_info["before_data"]["close"])
            except:
                continue
            try:
                price_open = float(earnings_info["after_data"]["open"])
            except:
                continue
            gap = gap_to_procent(close_day_before,price_open)
            price_high = float(earnings_info["after_data"]["high"])
            price_low = float(earnings_info["after_data"]["low"])
            close_day_of = float(earnings_info["after_data"]["close"])
            move_up = gap_to_procent(price_open,price_high)
            move_down = gap_to_procent(price_open,price_low)
            move_down = gap_to_procent(price_open,price_low)
            move_close = gap_to_procent(price_open,close_day_of)
            last_2_years[release_date]["gap"] = gap
            #gappers.append([stock,gap,move_up,move_down,move_close])
            #gaps.append(gap)
            #moves_up.append(move_up)
            #moves_down.append(move_down)
            moves = {}
            moves["gap"] = gap
            moves["move_up"] = move_up
            moves["move_down"] = move_down
            moves["move_close"] = move_close
            print(release_date,moves)
        
        #last_2_years["gaps"]=gaps
        for key, earnings_info in last_2_years.items():
            if type(earnings_info)==dict:
                for data,specific in earnings_info.items():
                    print(data,"=",specific)
            print("")
            if type(earnings_info)!=dict:
                print(key,"=",earnings_info)
        #gappers[stock]=moves  

              
    for a,val in enumerate(gappers):
        print(val)
        continue
        for b,val2 in enumerate(val):
            print(val2)

         
    for key, gap_info in gappers.items():
        if len(gap_info)==0:
            continue
        print("new",key,"=",gap_info)


        
            
                
            print("")
            print("release_date",release_date)
            try:
                for data,specific in earnings_info.items():
                    print(data,"=",specific)
            except:
                continue
        print("gaps",last_2_years["gaps"])
        print("------------------")
        print(last_2_years)
        print("------------------")
        """


import os,sys
stocks = get_stock_list("500.csv")
stocks = stocks[0:100]
for a,stock in enumerate(stocks):
    print(a,stock)
#get_sec_earn_dates(stocks)
#sec_1000_chars(stocks)
#price_history(stocks)
gen_trend(stocks,"sec-edgar-filings")
#mine_earn_dates(stocks)
#gen_check()


