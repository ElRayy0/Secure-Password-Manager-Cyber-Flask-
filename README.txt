SECURE PASSWORD MANAGER
=======================

A full-stack password management application built with Flask, featuring Fernet-based encryption 
and SQLite database storage. Designed for secure password storage with a simple web interface.

FEATURES
--------
- Web-based interface for adding and viewing passwords
- AES-128 Fernet encryption for secure password storage
- SQLite database persistence
- Simple two-step workflow: Add passwords and view stored entries
- Minimal, lightweight application

REQUIREMENTS
------------
- Python 3.7+
- Flask
- cryptography

INSTALLATION
------------
1. Install required dependencies:
   pip install flask cryptography

2. Clone or download the project files

RUNNING THE APPLICATION
-----------------------
1. Navigate to the project directory in your terminal/command prompt
2. Run the application:
   python Pwd-mngr.py

3. Open your web browser and go to:
   http://localhost:5000

USAGE
-----
1. HOME PAGE (http://localhost:5000):
   - Enter the site/service name (e.g., "example.com")
   - Enter the password
   - Click "Add" to store the encrypted password
   - Click "View stored entries" to see all saved passwords

2. STORED ENTRIES (http://localhost:5000/list):
   - View all stored site names and their encrypted password representations
   - Note: Passwords are displayed as encrypted blobs (not decrypted)

IMPORTANT SECURITY NOTES
------------------------
- The encryption key is generated fresh each time the app starts
- After restarting the app, previously stored passwords CANNOT be decrypted with a new key
- This application generates an ephemeral (temporary) encryption key for each session
- For production use, implement persistent encryption key management
- Do not use this in production without additional security measures
- Always run over HTTPS in production environments
- Consider implementing user authentication and authorization

FILES
-----
- Pwd-mngr.py: Main Flask application with routes and encryption logic
- passwords.db: SQLite database file (created on first run)
