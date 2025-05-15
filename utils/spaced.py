import datetime

def schedule_next_review(interval, previous_date=None):
    if not previous_date:
        previous_date = datetime.date.today()
    return previous_date + datetime.timedelta(days=interval)

# Example SM-2 logic could be added later

from datetime import date, timedelta
from .database import create_connection

def update_flashcard_review(flashcard_id, quality):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT interval, repetition, ease_factor FROM flashcards WHERE id = ?", (flashcard_id,))
    interval, repetition, ef = cursor.fetchone()

    # SM-2 Algorithm
    if quality >= 3:
        if repetition == 0:
            interval = 1
        elif repetition == 1:
            interval = 6
        else:
            interval = int(interval * ef)
        repetition += 1
    else:
        repetition = 0
        interval = 1

    ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    if ef < 1.3:
        ef = 1.3

    next_review_date = date.today() + timedelta(days=interval)

    cursor.execute('''
        UPDATE flashcards
        SET interval = ?, repetition = ?, ease_factor = ?, next_review = ?
        WHERE id = ?
    ''', (interval, repetition, ef, next_review_date, flashcard_id))
    
    conn.commit()
    conn.close()