import sqlite3

def create_connection():
    conn = sqlite3.connect("eduvision.db")
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            interval INTEGER DEFAULT 1,
            repetition INTEGER DEFAULT 0,
            ease_factor REAL DEFAULT 2.5,
            next_review DATE
        )
    ''')
    
    conn.commit()
    conn.close()

from datetime import date

def insert_flashcard(question, answer):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO flashcards (question, answer, next_review)
        VALUES (?, ?, ?)
    ''', (question, answer, date.today()))
    conn.commit()
    conn.close()

def get_due_flashcards():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, question, answer, interval, repetition, ease_factor FROM flashcards
        WHERE next_review <= date('now')
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows