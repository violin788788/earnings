import subprocess
import re
import sys
import os
def run_git_pull():
    """Runs git pull and returns (success, output)"""
    result = subprocess.run(
        ["git", "pull"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    return (result.returncode == 0, result.stdout)
def extract_conflicting_files(output):
    """Extracts filenames from git output that are blocking the pull"""
    files = []
    # Git outputs lines like:
    # "Please move or remove them before you merge."
    # and lists files with indentation
    for line in output.splitlines():
        line = line.strip()
        # simple heuristic: endswith .csv or any file that is indented
        if line.startswith("price_history/") or line.startswith("e_history/"):
            files.append(line)
    return files
def remove_files(files):
    """Deletes files one by one"""
    for f in files:
        if os.path.exists(f):
            print(f"Removing {f}")
            os.remove(f)
def main():
    success, output = run_git_pull()
    if success:
        print("git pull successful ✅")
        return
    print("git pull failed, checking for conflicting files...")
    sys.exit()
    files = extract_conflicting_files(output)
    if not files:
        print("No conflicting files found. Here is git output:")
        print(output)
        sys.exit(1)
    remove_files(files)
    print("\nRetrying git pull...\n")
    success, output = run_git_pull()
    if success:
        print("git pull successful after removing conflicting files ✅")
    else:
        print("git pull still failed. Git output:")
        print(output)

if __name__ == "__main__":
    main()
