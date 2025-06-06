from flask import Flask, request, redirect, url_for, render_template, session, send_from_directory, flash
from functools import wraps
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import sqlite3


# Configuration
app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
DB_FILE = 'templates/uploads/database.db'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database setup
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS apks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        filename TEXT NOT NULL,
                        downloads INTEGER DEFAULT 0,
                        filesize INTEGER,
                        uploaded_at TEXT
                    )''')
        conn.commit()

# Admin login required decorator
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Login required.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper


@app.route('/')
def home():
    return redirect(url_for('upload_page'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'nom718' and password == 'nom11234':
            session['logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('upload_page'))

        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_page():
    if request.method == 'POST':
        if 'apks' in request.files:
            uploaded_files = request.files.getlist('apks')
            for apk in uploaded_files:
                if apk:
                    filename = secure_filename(apk.filename)
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    apk.save(filepath)

                    filesize = os.path.getsize(filepath)
                    uploaded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    with sqlite3.connect(DB_FILE) as conn:
                        c = conn.cursor()
                        c.execute("INSERT INTO apks (filename, filesize, uploaded_at) VALUES (?, ?, ?)",
                                  (filename, filesize, uploaded_at))
                        conn.commit()
            flash('Files uploaded successfully!', 'success')
            return redirect(url_for('upload_page'))

    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT id, filename, downloads, filesize, uploaded_at FROM apks")
        apks = c.fetchall()

    return render_template('upload.html', apks=apks)


@app.route('/download/<int:apk_id>')

@app.route('/files')
@login_required
def list_apks():
    files = []
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT filename, downloads FROM apks")
        records = c.fetchall()

        for filename, downloads in records:
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.exists(filepath):
                stat = os.stat(filepath)
                files.append({
                    'name': filename,
                    'time': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'size': f"{stat.st_size / 1024:.2f} KB",
                    'downloads': downloads,
                    'download_link': url_for('download_apk', filename=filename)
                })

    return render_template('list_files.html', files=files)


@app.route('/edit/<int:apk_id>', methods=['GET', 'POST'])
@login_required
def edit_apk(apk_id):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()

        if request.method == 'POST':
            new_filename = secure_filename(request.form.get('filename'))
            c.execute("SELECT filename FROM apks WHERE id = ?", (apk_id,))
            old_filename = c.fetchone()[0]

            old_path = os.path.join(UPLOAD_FOLDER, old_filename)
            new_path = os.path.join(UPLOAD_FOLDER, new_filename)

            if os.path.exists(old_path):
                os.rename(old_path, new_path)

            c.execute("UPDATE apks SET filename = ? WHERE id = ?", (new_filename, apk_id))
            conn.commit()
            flash('Filename updated successfully!', 'success')
            return redirect(url_for('upload_page'))

        c.execute("SELECT * FROM apks WHERE id = ?", (apk_id,))
        apk = c.fetchone()
    return render_template('edit.html', apk=apk)


@app.route('/delete/<int:apk_id>', methods=['POST'])

@login_required
def delete_apk(apk_id):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT filename FROM apks WHERE id = ?", (apk_id,))
        apk = c.fetchone()
        if apk:
            filename = apk[0]
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
            c.execute("DELETE FROM apks WHERE id = ?", (apk_id,))
            conn.commit()
            flash('APK deleted successfully.', 'success')
        else:
            flash('APK not found.', 'danger')
    return redirect(url_for('upload_page'))



@app.route('/files')
@login_required
def list_files():
    files = []
    upload_dir = os.path.join(app.root_path, 'uploads')

    for filename in os.listdir(upload_dir):
        if filename.endswith('.apk'):
            filepath = os.path.join(upload_dir, filename)
            upload_time = datetime.fromtimestamp(os.path.getctime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
            size = os.path.getsize(filepath) // 1024  # Size in KB
            files.append({
                'name': filename,
                'time': upload_time,
                'size': f"{size} KB",
                'download_link': url_for('download_apk', filename=filename)
            })

    return render_template('list_files.html', files=files)

@app.route('/apks')
def public_apk_list():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT filename, downloads, filesize, uploaded_at FROM apks")
        apks = c.fetchall()
    return render_template('public_apks.html', apks=apks)

@app.route('/public_download/<filename>')
def public_download(filename):
    # Increase download count
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("UPDATE apks SET downloads = downloads + 1 WHERE filename = ?", (filename,))
        conn.commit()

    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/public')
def public_page():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT filename, downloads, filesize, uploaded_at FROM apks")
        apks = c.fetchall()
    return render_template('public_apks.html', apks=apks)

@app.route('/downloads/<filename>')
@login_required
def download_apk(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        flash("File not found.", "danger")
        return redirect(url_for('upload_page'))

    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("UPDATE apks SET downloads = downloads + 1 WHERE filename = ?", (filename,))
        conn.commit()

    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
