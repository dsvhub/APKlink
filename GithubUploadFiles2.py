import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext

# -------------------------
# CONFIG: Set your repo path
# -------------------------
REPO_PATH = r"F:/PycharmProjects/ISub/APKHostingApp/Mybuild/APKHostingApp3.0 - backup"
uploads = os.path.join(REPO_PATH, "uploads")


def run_git(cmd):
    """Run git command inside the repo."""
    result = subprocess.run(
        cmd,
        cwd=REPO_PATH,
        text=True,
        capture_output=True,
        shell=True
    )
    return result.stdout + result.stderr


# -------------------------
# REMOTE URL FUNCTIONS
# -------------------------

def get_remote_url():
    """Returns the current GitHub remote URL."""
    result = run_git("git remote get-url origin")
    return result.strip() if result.strip() else "No remote URL set"


def change_remote_url():
    """Change the GitHub repo remote URL."""
    current = get_remote_url()
    new_url = simpledialog.askstring(
        "Change GitHub Repo URL",
        f"Current URL:\n{current}\n\nEnter new GitHub URL:"
    )

    if new_url:
        run_git(f"git remote set-url origin {new_url}")
        remote_label.config(text=f"Remote URL: {new_url}")
        log_text.insert(tk.END, f"Changed remote URL to:\n{new_url}\n\n")
        log_text.see(tk.END)
        messagebox.showinfo("Updated", f"GitHub repo URL has been updated:\n{new_url}")


# -------------------------
# FILE UPLOAD
# -------------------------

def upload_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return

    if not os.path.exists(uploads):
        messagebox.showerror("Error", "Uploads folder does not exist!")
        return

    filename = os.path.basename(filepath)
    dest_path = os.path.join(uploads, filename)

    try:
        shutil.copy(filepath, dest_path)
        log_text.insert(tk.END, f"Copied: {filename}\n")
    except Exception as e:
        messagebox.showerror("Copy Error", str(e))
        return

    commit_msg = f"Add {filename}"

    git_output = ""
    git_output += run_git("git add .")
    git_output += run_git(f'git commit -m "{commit_msg}"')
    git_output += run_git("git pull origin main --rebase")
    git_output += run_git("git push origin main")

    log_text.insert(tk.END, git_output + "\n")
    log_text.see(tk.END)

    messagebox.showinfo("Success", f"{filename} uploaded to GitHub!")


# -------------------------
# GUI Layout
# -------------------------

root = tk.Tk()
root.title("GitHub File Uploader")
root.geometry("700x500")

frame = tk.Frame(root)
frame.pack(pady=10)

browse_btn = tk.Button(frame, text="Select File to Upload", font=("Arial", 14),
                       command=upload_file)
browse_btn.pack(pady=5)

# -------- SHOW REMOTE URL --------
remote_label = tk.Label(root, text=f"Remote URL: {get_remote_url()}", font=("Arial", 10))
remote_label.pack(pady=5)

change_remote_btn = tk.Button(root, text="Change GitHub Repo URL", font=("Arial", 12),
                              command=change_remote_url)
change_remote_btn.pack(pady=5)
# ---------------------------------

log_text = scrolledtext.ScrolledText(root, width=85, height=20, font=("Consolas", 10))
log_text.pack(pady=10)

root.mainloop()
