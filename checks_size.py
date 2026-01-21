import os,shutil


#folder_size(path)
def folder_size(path):
    from pathlib import Path
    return sum(f.stat().st_size for f in Path(path).rglob("*") if f.is_file())

dir_earnings = "sec-edgar-filings"
dir_prices = "price_history"

"""
folder_sizes = []
deleted = []
list_files = os.listdir(os.path.join(dir_earnings))
for a,stock in enumerate(list_files):
    folder_to_check = os.path.join(dir_earnings,stock)
    size = folder_size(folder_to_check)
    if size > 15000:
        shutil.rmtree(folder_to_check)
        print(f"{folder_to_check} deleted")
        deleted.append(folder_to_check)
    folder_sizes.append([size,folder_to_check])
    print(a,len(list_files),folder_to_check,folder_size(folder_to_check))
folder_sizes.sort()
for a,stock in enumerate(folder_sizes):
    print(stock)
print("deleted",deleted)
"""

folder_sizes = []
deleted = []
list_files = os.listdir(os.path.join(dir_prices))
for a,stock in enumerate(list_files):
    folder_to_check = os.path.join(dir_prices,stock)
    size = folder_size(folder_to_check)
    folder_sizes.append([size,folder_to_check])
    print(a,len(list_files),folder_to_check,folder_size(folder_to_check))
    continue
    if size > 15000:
        shutil.rmtree(folder_to_check)
        print(f"{folder_to_check} deleted")
        deleted.append(folder_to_check)
folder_sizes.sort()
for a,stock in enumerate(folder_sizes):
    print(stock)
print("deleted",deleted)