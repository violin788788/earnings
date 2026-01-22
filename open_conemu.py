import subprocess

# Path to ConEmu executable
conemu_path = r"C:\Program Files\ConEmu\ConEmu64.exe"  # Change if your path is different

# Directory you want ConEmu to open in
target_dir = r"A:\Users\-\0code\trading"

# Launch ConEmu in the specific directory
subprocess.run([conemu_path, "/dir", target_dir])
