##############################################################################
######Use this file to edit public html for my file sharing app v3.0##########
####### working script edit url entry fields, add spacing for each section ###
##############################################################################

import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
import subprocess

###################################


#################################

class FileHtmlEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Public File HTML GUI Editor")
        self.entries = []
        self.selected_row = None

        # Top Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="📂 Open HTML", command=self.load_html).pack(side="left", padx=5)
        tk.Button(button_frame, text="💾 Save HTML", command=self.save_html).pack(side="left", padx=5)
        tk.Button(button_frame, text="⬆️ Push to GitHub", command=self.git_push).pack(side="left", padx=5)
        tk.Button(button_frame, text="🖼️ Upload Icon", command=self.upload_icon).pack(side="left", padx=5)
        tk.Button(button_frame, text="➕ Add Row", command=self.add_row).pack(side="left", padx=5)

        # Scrollable Canvas for Rows
        self.scroll_canvas = tk.Canvas(root)
        self.scroll_frame = tk.Frame(self.scroll_canvas)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.scroll_canvas.yview)
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scroll_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_frame.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))

    def load_html(self):
        file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
        if not file_path:
            return
        self.file_path = file_path

        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        self.entries.clear()
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        rows = soup.select("table tr")[1:]
        for i, row in enumerate(rows):
            cols = row.find_all("td")
            if len(cols) != 3:
                continue

            file_title = cols[0].get_text(strip=True).replace("\n", "").split("APK")[0].strip()
            version = cols[1].text.strip()
            img_tag = cols[0].find("img")
            icon_path = img_tag["src"].split("filename='")[1].split("'")[0] if img_tag else ""
            url = cols[2].find("a")["href"]

            self._create_row(file_title, version, icon_path, url)

    def _create_row(self, name="", version="", icon="", url=""):
        index = len(self.entries)
        section = tk.Frame(self.scroll_frame, bd=2, relief="groove", padx=10, pady=10)
        section.pack(padx=10, pady=10, fill="x")
        section.bind("<Button-1>", lambda e, idx=index: self.select_row(idx))

        row = []

        tk.Label(section, text="File Title:").grid(row=0, column=0, sticky="e")
        name_entry = tk.Entry(section, width=40)
        name_entry.insert(0, name)
        name_entry.grid(row=0, column=1)
        row.append(name_entry)

        tk.Label(section, text="Version:").grid(row=1, column=0, sticky="e")
        version_entry = tk.Entry(section, width=20)
        version_entry.insert(0, version)
        version_entry.grid(row=1, column=1)
        row.append(version_entry)

        tk.Label(section, text="Icon Path:").grid(row=2, column=0, sticky="e")
        icon_entry = tk.Entry(section, width=60)
        icon_entry.insert(0, icon)
        icon_entry.grid(row=2, column=1)
        row.append(icon_entry)

        tk.Label(section, text="Download URL:").grid(row=3, column=0, sticky="e")
        url_entry = tk.Entry(section, width=90)
        url_entry.insert(0, url)
        url_entry.grid(row=3, column=1)
        row.append(url_entry)

        self.entries.append(row)

        self.root.update_idletasks()
        self.scroll_canvas.yview_moveto(1.0)

    def select_row(self, index):
        self.selected_row = index
        for i, section in enumerate(self.scroll_frame.winfo_children()):
            section.config(bg="#e6f7ff" if i == index else "SystemButtonFace")

    def add_row(self):
        self._create_row()

    def save_html(self):
        if not hasattr(self, "file_path"):
            messagebox.showerror("Error", "No HTML file loaded.")
            return

        with open(self.file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        table = soup.find("table")
        for tr in table.find_all("tr")[1:]:
            tr.decompose()

        for row in self.entries:
            name, version, icon, url = [e.get().strip() for e in row]

            new_tr = soup.new_tag("tr")

            td1 = soup.new_tag("td")
            img_tag = soup.new_tag("img", src="{{ url_for('static', filename='" + icon + "') }}", alt="Logo")
            img_tag["style"] = "height:40px; vertical-align: middle; margin-right: 10px;"
            td1.append(img_tag)
            td1.append(soup.new_string(" " + name))
            new_tr.append(td1)

            td2 = soup.new_tag("td")
            td2.string = version
            new_tr.append(td2)

            td3 = soup.new_tag("td")
            a_tag = soup.new_tag("a", href=url, **{"class": "btn-download", "target": "_blank"})
            a_tag.string = "Download"
            td3.append(a_tag)
            new_tr.append(td3)

            table.append(new_tr)

        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(str(soup.prettify()))
        messagebox.showinfo("Saved", "HTML updated successfully.")

    def git_push(self):
        if not hasattr(self, "file_path"):
            messagebox.showerror("Error", "No HTML file loaded.")
            return

        folder = os.path.dirname(self.file_path)
        try:
            subprocess.check_call(["git", "add", "."], cwd=folder)
            subprocess.check_call(["git", "commit", "-m", "Update HTML from GUI"], cwd=folder)
            subprocess.check_call(["git", "push"], cwd=folder)
            messagebox.showinfo("Git", "Changes pushed to GitHub.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Git Error", f"An error occurred:\n{e}")

    def upload_icon(self):
        if self.selected_row is None:
            messagebox.showwarning("No Row Selected", "Please click on a row before uploading an icon.")
            return

        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
        if not filepath:
            return

        filename = os.path.basename(filepath)
        target_dir = os.path.join(os.path.dirname(self.file_path), "static", "icons")
        os.makedirs(target_dir, exist_ok=True)
        target_path = os.path.join(target_dir, filename)

        try:
            shutil.copy(filepath, target_path)
            self.entries[self.selected_row][2].delete(0, tk.END)
            self.entries[self.selected_row][2].insert(0, f"icons/{filename}")
            messagebox.showinfo("Success", f"Icon uploaded to {target_path}")
        except Exception as e:
            messagebox.showerror("Upload Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FileHtmlEditor(root)
    root.mainloop()