import os
import subprocess

conemu_path = r"C:\Program Files\ConEmu\ConEmu64.exe"  # Change if your path is different

cwd = os.getcwd()
subprocess.run([conemu_path, "/dir", cwd])
