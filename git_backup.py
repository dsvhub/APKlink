import subprocess

def run_git_command(cmd):
    """Run a git command and print output or error."""
    try:
        result = subprocess.run(cmd, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running {' '.join(cmd)}:\n{e.stderr}")

def git_backup(commit_message="Backup commit", branch="main"):
    print("Staging all files...")
    run_git_command(["git", "add", "."])

    print(f"Committing with message: {commit_message}")
    run_git_command(["git", "commit", "-m", commit_message])

    print(f"Pushing to branch {branch}...")
    run_git_command(["git", "push", "origin", branch])

if __name__ == "__main__":
    commit_msg = input("Enter commit message (or press enter for default): ").strip()
    if not commit_msg:
        commit_msg = "Backup commit"

    branch_name = input("Enter branch name to push to (default 'main'): ").strip()
    if not branch_name:
        branch_name = "main"

    git_backup(commit_message=commit_msg, branch=branch_name)
