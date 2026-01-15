#du -sh earnings/*/ | sort -hr
import os,sys
folder_sec = "sec-edgar-filings"
dirs = os.listdir(folder_sec)
for val in dirs:
    #print(val)
    directory = os.path.join(folder_sec,val)
    commands = [
        "du -sh "+directory+"/ | sort -hr"
    ]
    for command in commands:
        back = str(os.system(command))

        #print(back)
        #os.system(command)







"""
commands = [
    "du -sh sec-edgar-filings/*/ | sort -hr"
]
# Execute the commands in the shell using os.system()
"""