#du -sh earnings/*/ | sort -hr

import os
commands = [
    "du -sh sec-edgar-filings/*/ | sort -hr"
]
print("adding files")
# Execute the commands in the shell using os.system()
for command in commands:
    os.system(command)
