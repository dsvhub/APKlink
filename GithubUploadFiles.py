import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# -------------------------
# CONFIG: Set your repo path
# -------------------------
REPO_PATH = r"F:/PycharmProjects/ISub/APKHostingApp/Mybuild/APKHostingApp3.0 - backup"   # <-- CHANGE THIS!
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

    # Commit and push
    commit_msg = f"Add {filename}"

    git_output = ""
    git_output += run_git("git add .")
    git_output += run_git(f'git commit -m "{commit_msg}"')
    git_output += run_git("git push origin main")

    log_text.insert(tk.END, git_output + "\n")
    log_text.see(tk.END)

    messagebox.showinfo("Success", f"{filename} uploaded to GitHub!")


# -------------------------
# GUI Layout
# -------------------------
root = tk.Tk()
root.title("GitHub File Uploader")
root.geometry("600x450")

frame = tk.Frame(root)
frame.pack(pady=10)

browse_btn = tk.Button(frame, text="Select File to Upload", font=("Arial", 14),
                       command=upload_file)
browse_btn.pack()

log_text = scrolledtext.ScrolledText(root, width=70, height=20, font=("Consolas", 10))
log_text.pack(pady=10)

root.mainloop()
