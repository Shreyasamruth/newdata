import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail SMTP Configuration with User's App Password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "pswx.security.ai@gmail.com"
GMAIL_APP_PASSWORD = "vgiq rabg yydr pkfh".replace(" ", "")

def send_otp_email(recipient_email: str, otp_code: str, recipient_name: str = "User") -> bool:
    """Sends a real email verification OTP code via Gmail SMTP using App Password."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🔐 {otp_code} is your PSWX AI Security Verification Code"
        msg["From"] = f"PSWX Security Engine <{SENDER_EMAIL}>"
        msg["To"] = recipient_email

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f4ff; margin: 0; padding: 20px; }}
            .container {{ max-width: 500px; margin: 0 auto; background: #ffffff; padding: 30px; border-radius: 16px; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,82,255,0.08); }}
            .logo {{ font-size: 24px; font-weight: 800; color: #0052ff; text-align: center; margin-bottom: 20px; }}
            .otp-box {{ font-size: 32px; font-weight: 900; color: #0052ff; letter-spacing: 8px; text-align: center; padding: 15px; background: #f0f4ff; border-radius: 12px; margin: 20px 0; border: 2px dashed #0052ff; }}
            .footer {{ font-size: 12px; color: #64748b; text-align: center; margin-top: 25px; border-top: 1px solid #e2e8f0; padding-top: 15px; }}
          </style>
        </head>
        <body>
          <div class="container">
            <div class="logo">PSWX <span>AI</span> SECURITY</div>
            <p>Hello <b>{recipient_name}</b>,</p>
            <p>Your 6-digit email verification OTP code to complete authentication is:</p>
            <div class="otp-box">{otp_code}</div>
            <p>Enter this code on the PSWX AI verification screen to complete your login.</p>
            <div class="footer">
              This code was requested for <b>{recipient_email}</b>. If you did not request this code, please ignore this email.
            </div>
          </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_content, "html"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.starttls()
        server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        server.quit()
        print(f"Real Email OTP successfully sent to {recipient_email}")
        return True
    except Exception as e:
        print(f"SMTP Real Email Sending Note/Error ({e}): Falling back to display mode.")
        return False
