import os,subprocess,sys,platform
cwd = os.getcwd()
directory_name = os.path.basename(cwd)
print(directory_name)
print(cwd)
system_type = platform.system()
print(type(system_type))
print(system_type)
if "Linux" in system_type:
    print("do not open chrome")

#print system type



#"git push origin main --force"

# Define the Git commands
commands = [
    "git add -A",
    'git commit -m "update/create/delete files+folders"'
]

# Execute the commands in the shell using os.system()
for command in commands:
    os.system(command)

# Step 1: Read the token from the token.txt file
with open('token.txt', 'r') as file:
    token = file.read().strip()  # Read the token and remove any extra whitespace
# Step 2: Set up the GitHub repository URL with the token for authentication
repo_url = f"https://{token}@github.com/violin788788/"+directory_name+".git"

# Step 3: Execute the Git command (force push)
try:
    # Run the git push command with the token for authentication
    subprocess.run(["git", "push", repo_url, "main", "--force"], check=True)
    print("Force push to GitHub was successful!")
except subprocess.CalledProcessError as e:
    print(f"Error occurred: {e}")




from datetime import datetime
timestamp=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
iden_last_pushed="git-push"
for f in os.listdir("."):
    if iden_last_pushed in f and f.endswith(".txt") and os.path.isfile(f):
        os.remove(f)
filename=f"{iden_last_pushed}-{timestamp}.txt"
with open(filename,"w") as f:
    f.write("Hello, this is the output.\n")
print(f"Created file: {filename}")



sys.exit()

if "Linux" in system_type:
    print("do not open chrome")
    sys.exit()

url = r"https://github.com/violin788788/"+directory_name
chrome_path = r"A:\Program Files\Google\Chrome\Application\chrome.exe"
subprocess.run([chrome_path, "--incognito", url])


"""
create git
git init

create main branch
git checkout -b main

add remote
git remote add origin https://github.com/violin788788/"+directory_name+".git"

stage all changes
git add -A

commit changes
git commit -m "Remove unwanted files and directories, and add/modify other changes"

force?
git push origin main --force

username
violin788788
token


remove tracking
git rm --cached .lesshst


"""