import subprocess
import sys

# Change this if your branch is not 'main'
BRANCH = "main"

def run(cmd):
    """Run a shell command and print output."""
    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print("Command failed:", e)
        sys.exit(1)

def main():
    print(f"Fetching latest changes from origin/{BRANCH}...")
    run("git fetch origin")

    print(f"Resetting local branch '{BRANCH}' to match origin/{BRANCH}...")
    run(f"git reset --hard origin/{BRANCH}")

    print("Removing untracked files and directories...")
    run("git clean -fd")

    print("Current branch status:")
    run("git status")

    print("\n✅ Update complete! Server now matches GitHub exactly, including deleted folders.")

if __name__ == "__main__":
    main()




from datetime import datetime
timestamp=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
iden_last_pushed="git-pull"
for f in os.listdir("."):
    if iden_last_pushed in f and f.endswith(".txt") and os.path.isfile(f):
        os.remove(f)
filename=f"{iden_last_pushed}-{timestamp}.txt"
with open(filename,"w") as f:
    f.write("Hello, this is the output.\n")
print(f"Created file: {filename}")

