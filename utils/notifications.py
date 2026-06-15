import smtplib
from email.mime.text import MIMEText
import os

def send_appointment_reminder(email, appointment_data):
    """Send appointment reminder email."""
    
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    sender_email = os.environ.get("SENDER_EMAIL", "")
    sender_password = os.environ.get("SENDER_PASSWORD", "")
    
    message = f"""
    Hello,
    
    This is a reminder about your upcoming ClarityNet appointment:
    
    Program: {appointment_data['program']}
    Date: {appointment_data['date']}
    Time: {appointment_data['time']}
    
    Please arrive 10 minutes early.
    
    Best regards,
    ClarityNet Team
    """
    
    msg = MIMEText(message)
    msg['Subject'] = f"Reminder: Your {appointment_data['program']} Appointment"
    msg['From'] = sender_email
    msg['To'] = email
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False