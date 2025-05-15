import smtplib
from email.mime.text import MIMEText
from utils.database import get_due_flashcards

def send_email_reminder(to_email):
    due_cards = get_due_flashcards()
    
    if not due_cards:
        return "No flashcards due today."

    body = "Here are your due flashcards for today:\n\n"
    for card in due_cards:
        body += f"Q: {card[1]}\nA: {card[2]}\n\n"

    msg = MIMEText(body)
    msg['Subject'] = "Your EduVision Flashcards – Review Reminder"
    msg['From'] = "your.email@gmail.com"
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login("your.email@gmail.com", "your-app-password")
        server.send_message(msg)

    return "Email sent!"