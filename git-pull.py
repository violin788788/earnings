import subprocess

# Step 1: pull from origin/main
subprocess.run(["git", "pull", "origin", "main"], check=True)
