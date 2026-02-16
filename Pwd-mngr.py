from flask import Flask, request, render_template_string
from cryptography.fernet import Fernet
import sqlite3

app = Flask(__name__)

# Generate a Fernet key for symmetric encryption.
# NOTE: This key is generated each time the app starts, so stored
# encrypted passwords cannot be decrypted after a restart.
fernet_key = Fernet.generate_key()
fernet_cipher = Fernet(fernet_key)


def _ensure_db_table(conn):
    """Create the passwords table if it doesn't exist."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS pwds (
            site TEXT NOT NULL,
            pwd BLOB NOT NULL
        )
        """
    )


@app.route('/', methods=['GET', 'POST'])
def home():
    """Handle adding a site and its encrypted password."""
    if request.method == 'POST':
        # Read form inputs (plain text)
        site_name = request.form['site']
        password_plain = request.form['pwd']

        # Encrypt the password before storing
        password_encrypted = fernet_cipher.encrypt(password_plain.encode())

        # Persist to SQLite database (ensure table exists first)
        db_conn = sqlite3.connect('passwords.db')
        _ensure_db_table(db_conn)
        db_conn.execute("INSERT INTO pwds (site, pwd) VALUES (?, ?)", (site_name, password_encrypted))
        db_conn.commit()
        db_conn.close()

    # Minimal form rendered inline for simplicity
    return render_template_string(
        '''<form method=post>Site: <input name=site><br>Password: <input name=pwd type=password><br><button>Add</button></form>'''
    )


if __name__ == '__main__':
    app.run()