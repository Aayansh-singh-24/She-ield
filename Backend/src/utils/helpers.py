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


def send_emergency_email(to_email: str, recipient_name: str, user_name: str, tracking_url: str, custom_message: str):
    """
    Sends an urgent HTML emergency alert email with live location tracking link.
    """
    if not setting.SMTP_USERNAME or not setting.SMTP_PASSWORD:
        print(f"[Mail Dev Mode] Emergency alert for {to_email} from {user_name}: {tracking_url}")
        return

    msg = MIMEMultipart()
    sender = setting.SMTP_FROM_EMAIL or setting.SMTP_USERNAME
    msg['From'] = f"She-ield Emergency Alert <{sender}>"
    msg['To'] = to_email
    msg['Subject'] = f"🚨 EMERGENCY ALERT: {user_name} needs immediate assistance!"

    body_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; margin: 0; padding: 20px; }}
        .card {{ max-width: 580px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; border: 2px solid #ef4444; box-shadow: 0 10px 25px rgba(239, 68, 68, 0.15); }}
        .header {{ background: #dc2626; color: #ffffff; padding: 24px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; letter-spacing: 1px; }}
        .content {{ padding: 24px; color: #1e293b; line-height: 1.6; }}
        .alert-box {{ background: #fef2f2; border-left: 4px solid #ef4444; padding: 16px; border-radius: 6px; margin: 18px 0; }}
        .button {{ display: inline-block; background-color: #dc2626; color: #ffffff !important; padding: 16px 32px; font-size: 16px; font-weight: bold; text-decoration: none; border-radius: 8px; text-align: center; margin: 20px 0; box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3); }}
        .footer {{ padding: 16px 24px; background: #f1f5f9; text-align: center; font-size: 13px; color: #64748b; }}
      </style>
    </head>
    <body>
      <div class="card">
        <div class="header">
          <h1>🚨 SHE-IELD EMERGENCY ALERT</h1>
        </div>
        <div class="content">
          <p>Hello <strong>{recipient_name}</strong>,</p>
          <p><strong>{user_name}</strong> has triggered an emergency SOS alert and requires immediate assistance.</p>
          
          <div class="alert-box">
            <strong>Message from {user_name}:</strong><br>
            <p style="margin: 8px 0 0 0; font-size: 16px; color: #991b1b;">"{custom_message or 'I need immediate help.'}"</p>
          </div>

          <div style="text-align: center;">
            <a href="{tracking_url}" class="button" target="_blank">📍 TRACK LIVE LOCATION NOW</a>
          </div>

          <p style="font-size: 13px; color: #64748b; word-break: break-all;">
            If the button above does not work, copy and paste this link in your browser:<br>
            <a href="{tracking_url}">{tracking_url}</a>
          </p>
        </div>
        <div class="footer">
          This is an automated safety alert dispatched by She-ield Emergency System.
        </div>
      </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(body_html, 'html'))

    try:
        with smtplib.SMTP(setting.SMTP_HOST, setting.SMTP_PORT) as server:
            server.starttls()
            server.login(setting.SMTP_USERNAME, setting.SMTP_PASSWORD)
            server.sendmail(sender, to_email, msg.as_string())
        print(f"[SUCCESS] Emergency Email sent successfully to {to_email}")
    except Exception as e:
        print(f"[ERROR] Failed to send emergency email to {to_email}: {str(e)}")
