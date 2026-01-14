import sys,os
from sec_edgar_downloader import Downloader
dl = Downloader("YourCompanyName", "your@email.com")

stock = "msft"

stock = stock.upper()
print(stock)

cwd = os.getcwd()
print (cwd)


def char_1000(stock):
    folder_yearly = os.path.join("sec-edgar-filings",stock,"10-K")
    folder_quarterly = os.path.join("sec-edgar-filings",stock,"10-Q")
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
    load the txts..and then rewrite them with only first 1000 chars..

    """

char_1000(stock)


sys.exit()

print(stock+" getting quarterly reports")
# Quarterly reports (10-Q)
dl.get("10-Q", stock, after="2022-01-01", before="2025-01-01")
print(stock+" getting yearly reports")
# Annual reports (10-K)
dl.get("10-K", stock, after="2022-01-01", before="2025-01-01")
