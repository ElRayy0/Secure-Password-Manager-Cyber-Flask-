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


def init_db(db_path='passwords.db'):
    """Initialize the database file and ensure required tables exist."""
    conn = sqlite3.connect(db_path)
    _ensure_db_table(conn)
    conn.close()


def encrypt_password(plain_text_password: str) -> bytes:
    """Return the encrypted bytes for a plaintext password."""
    return fernet_cipher.encrypt(plain_text_password.encode())


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
        '''<h1>Password Manager</h1>
        <form method="post">Site: <label><input name="site" placeholder="example.com" required></label><br>Password: <label><input name="pwd" type="password" required></label><br><button type="submit">Add</button></form>
        <p><a href="/list">View stored entries</a></p>'''
    )


@app.route('/list', methods=['GET'])
def list_pwds():
    """Return a simple list of stored sites and their encrypted blobs.

    Note: stored passwords are shown as their encrypted representation
    (not decrypted) because the app currently generates a new ephemeral key
    at each start.
    """
    conn = sqlite3.connect('passwords.db')
    _ensure_db_table(conn)
    cur = conn.execute("SELECT site, pwd FROM pwds")
    rows = cur.fetchall()
    conn.close()

    items = "".join(f"<li>{r[0]}: {repr(r[1])}</li>" for r in rows)
    return render_template_string(f"<h2>Stored passwords</h2><ul>{items}</ul>")


if __name__ == '__main__':
    # Initialize DB before starting the server so the table exists.
    init_db()
 