import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional
from core.config import settings

logger = logging.getLogger("auth.email")


class EmailService:
    def __init__(self):
        self.dev_mode = settings.EMAIL_DEV_MODE or not bool(settings.SMTP_HOST)
        self.frontend_url = settings.FRONTEND_URL.rstrip("/")

    def send_verification_email(self, recipient_email: str, full_name: str, raw_token: str) -> bool:
        """Send account email verification link."""
        verification_link = f"{self.frontend_url}/verify-email?token={raw_token}"
        subject = f"Verify your {settings.PROJECT_NAME} account"
        
        text_content = (
            f"Hello {full_name},\n\n"
            f"Thank you for creating an account with {settings.PROJECT_NAME}.\n"
            f"Please verify your email address by visiting this link (expires in {settings.EMAIL_VERIFICATION_EXPIRE_HOURS} hours):\n"
            f"{verification_link}\n\n"
            f"If you did not create this account, please ignore this email.\n"
        )
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #09090d; color: #f4f4f8; margin: 0; padding: 30px; }}
            .container {{ max-width: 560px; margin: 0 auto; background: #111116; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 32px; }}
            .brand {{ font-size: 20px; font-weight: 700; background: linear-gradient(135deg, #f97316, #ec4899, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
            .btn {{ display: inline-block; background: linear-gradient(135deg, #f97316, #ec4899, #8b5cf6); color: #ffffff !important; padding: 12px 28px; text-decoration: none; border-radius: 8px; font-weight: 600; margin-top: 20px; }}
            .footer {{ font-size: 12px; color: #647082; margin-top: 30px; border-top: 1px solid rgba(255,255,255,0.07); padding-top: 16px; }}
          </style>
        </head>
        <body>
          <div class="container">
            <div class="brand">{settings.PROJECT_NAME}</div>
            <h2>Verify your email address</h2>
            <p>Hi {full_name},</p>
            <p>Please confirm your email address to activate all security features and AI tools on your account.</p>
            <p><a href="{verification_link}" class="btn">Verify Email Address</a></p>
            <p style="font-size: 13px; color: #9aa3b2;">Or copy and paste this link into your browser:<br/><span style="color: #a78bfa; word-break: break-all;">{verification_link}</span></p>
            <div class="footer">
              This link will expire in {settings.EMAIL_VERIFICATION_EXPIRE_HOURS} hours. If you did not sign up for {settings.PROJECT_NAME}, you can safely disregard this message.
            </div>
          </div>
        </body>
        </html>
        """
        
        return self._send_email(recipient_email, subject, text_content, html_content, preview_link=verification_link)

    def send_password_reset_email(self, recipient_email: str, full_name: str, raw_token: str) -> bool:
        """Send password reset link with single-use token."""
        reset_link = f"{self.frontend_url}/reset-password?token={raw_token}"
        subject = f"Reset your {settings.PROJECT_NAME} password"
        
        text_content = (
            f"Hello {full_name},\n\n"
            f"A password reset request was received for your {settings.PROJECT_NAME} account.\n"
            f"Reset your password by clicking this link (valid for {settings.PASSWORD_RESET_EXPIRE_HOURS} hour):\n"
            f"{reset_link}\n\n"
            f"If you did not request this, please secure your account immediately.\n"
        )
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #09090d; color: #f4f4f8; margin: 0; padding: 30px; }}
            .container {{ max-width: 560px; margin: 0 auto; background: #111116; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 32px; }}
            .brand {{ font-size: 20px; font-weight: 700; background: linear-gradient(135deg, #f97316, #ec4899, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
            .btn {{ display: inline-block; background: linear-gradient(135deg, #f97316, #ec4899, #8b5cf6); color: #ffffff !important; padding: 12px 28px; text-decoration: none; border-radius: 8px; font-weight: 600; margin-top: 20px; }}
            .footer {{ font-size: 12px; color: #647082; margin-top: 30px; border-top: 1px solid rgba(255,255,255,0.07); padding-top: 16px; }}
          </style>
        </head>
        <body>
          <div class="container">
            <div class="brand">{settings.PROJECT_NAME}</div>
            <h2>Password Reset Request</h2>
            <p>Hi {full_name},</p>
            <p>We received a request to reset your password. Click the button below to choose a new password.</p>
            <p><a href="{reset_link}" class="btn">Reset Password</a></p>
            <p style="font-size: 13px; color: #9aa3b2;">Or copy and paste this link into your browser:<br/><span style="color: #a78bfa; word-break: break-all;">{reset_link}</span></p>
            <div class="footer">
              This link expires in {settings.PASSWORD_RESET_EXPIRE_HOURS} hour. If you did not request a password reset, please ignore this email.
            </div>
          </div>
        </body>
        </html>
        """
        
        return self._send_email(recipient_email, subject, text_content, html_content, preview_link=reset_link)

    def _send_email(
        self,
        recipient_email: str,
        subject: str,
        text_content: str,
        html_content: str,
        preview_link: Optional[str] = None
    ) -> bool:
        """Internal email sender supporting development logging mode and production SMTP."""
        if self.dev_mode:
            logger.info("================== [DEV EMAIL SERVICE] ==================")
            logger.info("To: %s", recipient_email)
            logger.info("Subject: %s", subject)
            if preview_link:
                logger.info("Action Link: %s", preview_link)
            logger.info("=========================================================")
            print(f"\n[DEV EMAIL] To: {recipient_email} | Subject: {subject}\n[DEV EMAIL] Link: {preview_link}\n")
            return True

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
            msg["To"] = recipient_email
            
            msg.attach(MIMEText(text_content, "plain"))
            msg.attach(MIMEText(html_content, "html"))
            
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
                if settings.SMTP_TLS:
                    server.starttls()
                if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
                    server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                server.sendmail(settings.EMAILS_FROM_EMAIL, [recipient_email], msg.as_string())
            logger.info("Email delivered successfully to %s", recipient_email)
            return True
        except Exception as e:
            logger.error("Failed to deliver email to %s: %s", recipient_email, str(e))
            return False


email_service = EmailService()
