import subprocess

# Step 1: pull from origin/main
subprocess.run(["git", "pull", "origin", "main"], check=True)

# Step 2: get the previous HEAD before the pull
# HEAD@{1} is the previous position of HEAD
result = subprocess.run(
    ["git", "diff", "--name-only", "HEAD@{1}", "HEAD"],
    capture_output=True,
    text=True,
    check=True
)

# Step 3: print changed files
changed_files = result.stdout.strip().split("\n")
print("Files changed by this pull:")
for file in changed_files:
    print(file)
