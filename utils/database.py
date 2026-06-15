import json
import os
import sqlite3
from datetime import datetime

def init_database():
    """Initialize SQLite database."""
    conn = sqlite3.connect('claritynet.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        created_at TEXT,
        updated_at TEXT,
        profile_data TEXT,
        language TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        role TEXT,
        content TEXT,
        timestamp TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        filename TEXT,
        file_path TEXT,
        uploaded_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        program_id TEXT,
        status TEXT,
        submitted_at TEXT,
        updated_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    ''')
    
    conn.commit()
    conn.close()

def save_user_data(user_id, data):
    """Save user data."""
    init_database()
    conn = sqlite3.connect('claritynet.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT OR REPLACE INTO users (user_id, created_at, updated_at, profile_data)
    VALUES (?, ?, ?, ?)
    ''', (user_id, datetime.now().isoformat(), datetime.now().isoformat(), json.dumps(data)))
    
    conn.commit()
    conn.close()

def load_user_profile(user_id):
    """Load user profile."""
    init_database()
    conn = sqlite3.connect('claritynet.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT profile_data FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return json.loads(result[0])
    return {}

def save_document(user_id, file):
    """Save document info."""
    init_database()
    conn = sqlite3.connect('claritynet.db')
    cursor = conn.cursor()
    
    # Save file
    os.makedirs(f"data/documents/{user_id}", exist_ok=True)
    file_path = f"data/documents/{user_id}/{file.name}"
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    
    # Save to database
    cursor.execute('''
    INSERT INTO documents (user_id, filename, file_path, uploaded_at)
    VALUES (?, ?, ?, ?)
    ''', (user_id, file.name, file_path, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def get_documents(user_id):
    """Get user's documents."""
    init_database()
    conn = sqlite3.connect('claritynet.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT filename, file_path, uploaded_at FROM documents WHERE user_id = ?', (user_id,))
    results = cursor.fetchall()
    conn.close()
    
    return results