# In src/utils/helpers.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.utils.settings import setting

def send_otp_email(to_email: str, otp_code: str):
    if not setting.SMTP_USERNAME or not setting.SMTP_PASSWORD:
        print(f"[Mail Dev Mode] OTP for {to_email} is: {otp_code}")
        return

    msg = MIMEMultipart()
    msg['From'] = setting.SMTP_FROM_EMAIL or setting.SMTP_USERNAME
    msg['To'] = to_email
    msg['Subject'] = "She-ield - Verify Your Email"

    body = f"""
    <h2>Welcome to She-ield!</h2>
    <p>Please use the following One-Time Password (OTP) to verify your account:</p>
    <h1 style="color:#4F46E5; letter-spacing: 2px;">{otp_code}</h1>
    <p>This code is valid for 10 minutes. If you did not request this code, please ignore this email.</p>
    """
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP(setting.SMTP_HOST, setting.SMTP_PORT) as server:
            server.starttls()
            server.login(setting.SMTP_USERNAME, setting.SMTP_PASSWORD)
            server.sendmail(msg['From'], to_email, msg.as_string())
        print(f"OTP Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")