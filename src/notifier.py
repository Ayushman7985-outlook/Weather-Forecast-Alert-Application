"""Optional email notification (needs EMAIL_* values in .env)."""
import smtplib
from email.mime.text import MIMEText

from .config import get_email_settings


def send_email_alert(subject, body):
    """Send an email. Returns (ok: bool, message: str). Never raises."""
    cfg = get_email_settings()
    if cfg is None:
        return False, "Email not configured (fill EMAIL_* in .env). Skipped."
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"], msg["From"], msg["To"] = subject, cfg["sender"], cfg["receiver"]
    try:
        with smtplib.SMTP(cfg["server"], cfg["port"], timeout=15) as server:
            server.starttls()
            server.login(cfg["sender"], cfg["password"])
            server.send_message(msg)
        return True, f"Email sent to {cfg['receiver']}"
    except Exception as exc:  # network, auth, etc.
        return False, f"Email failed: {exc}"
