import schedule
import time
from utils.emailer import send_email_reminder

def job():
    send_email_reminder("student.email@example.com")

# Schedule every day at 8 AM
schedule.every().day.at("08:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)