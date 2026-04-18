import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
load_dotenv()

# ── Mailtrap credentials ──────────────────────────────────────────
# Store these in a .env file and load with python-dotenv in production.
# pip install python-dotenv
MAILTRAP_HOST = os.getenv("MAILTRAP_HOST")
MAILTRAP_PORT = int(os.getenv("MAILTRAP_PORT"))
MAILTRAP_USER = os.getenv("MAILTRAP_USER")   # ← replace
MAILTRAP_PASS = os.getenv("MAILTRAP_PASS")   # ← replace
SENDER_EMAIL  = os.getenv("SENDER_EMAIL")

# ─────────────────────────────────────────────────────────────────
#  LOW-LEVEL HELPER  –  sends one email (HTML + plain-text fallback)
# ─────────────────────────────────────────────────────────────────
def _send_email(to_email: str, subject: str, html_body: str, text_body: str) -> None:
    """
    Internal helper – never call this directly from a route.
    Creates a multipart/alternative message so clients that
    cannot render HTML still see readable plain text.
    """
    msg = MIMEMultipart("alternative")   # 'alternative' = HTML or text
    msg["Subject"] = subject
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = to_email

    # Attach plain-text first (lower priority), HTML second (higher priority).
    # Email clients always pick the LAST part they can render.
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    # Connect to Mailtrap sandbox via SMTP
    with smtplib.SMTP(MAILTRAP_HOST, MAILTRAP_PORT) as server:
        server.starttls()                              # encrypt the connection
        server.login(MAILTRAP_USER, MAILTRAP_PASS)    # authenticate
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

    print(f"[EmailService] ✅ Email sent → {to_email} | Subject: {subject}")

def _html_card(title: str, body_html: str, footer_note: str = "") -> str:
    """
    Wraps content in a clean, centred card.
    Inline CSS is used because many email clients strip <style> tags.
    Mailtrap sandbox DOES support HTML – you will see it rendered
    in the Mailtrap web inbox.
    """
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
    <body style="margin:0;padding:0;background:#f4f6f9;font-family:Arial,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0"
             style="background:#f4f6f9;padding:40px 0;">
        <tr>
          <td align="center">

            <!-- ── Card ── -->
            <table width="520" cellpadding="0" cellspacing="0"
                   style="background:#ffffff;border-radius:10px;
                          box-shadow:0 2px 12px rgba(0,0,0,.08);
                          overflow:hidden;">

              <!-- Header band -->
              <tr>
                <td style="background:#4F46E5;padding:28px 36px;">
                  <h1 style="margin:0;color:#ffffff;font-size:22px;
                             font-weight:700;letter-spacing:.5px;">
                    {title}
                  </h1>
                </td>
              </tr>

              <!-- Body -->
              <tr>
                <td style="padding:32px 36px;color:#374151;font-size:15px;
                           line-height:1.7;">
                  {body_html}
                </td>
              </tr>

              <!-- Footer -->
              <tr>
                <td style="background:#f9fafb;padding:18px 36px;
                           border-top:1px solid #e5e7eb;
                           color:#9ca3af;font-size:12px;text-align:center;">
                  {footer_note or "© 2025 MyApp &nbsp;·&nbsp; You received this because you have an account with us."}
                </td>
              </tr>

            </table>
            <!-- ── /Card ── -->

          </td>
        </tr>
      </table>
    </body>
    </html>
    """


# ─────────────────────────────────────────────────────────────────
#  1.  WELCOME EMAIL  –  triggered on create_user()
# ─────────────────────────────────────────────────────────────────
def send_welcome_email(name: str, email: str) -> None:
    subject = "🎉 Welcome to MyApp!"

    body_html = f"""
        <p>Hi <strong>{name}</strong>,</p>
        <p>We're thrilled to have you on board! Your account has been
           created successfully.</p>

        <table cellpadding="0" cellspacing="0"
               style="margin:24px 0;background:#f0f4ff;border-radius:8px;
                      border-left:4px solid #4F46E5;padding:16px 20px;
                      width:100%;">
          <tr>
            <td>
              <p style="margin:0 0 6px;color:#6b7280;font-size:13px;">
                YOUR ACCOUNT DETAILS
              </p>
              <p style="margin:0;font-size:15px;">
                <strong>Name&nbsp;&nbsp;:</strong> {name}<br>
                <strong>Email&nbsp;&nbsp;:</strong> {email}
              </p>
            </td>
          </tr>
        </table>

        <p>If you have any questions, just reply to this email – we're
           always happy to help.</p>
        <p style="margin-top:28px;">Cheers,<br>
           <strong>The MyApp Team</strong> 🚀</p>
    """

    text_body = (
        f"Hi {name},\n\n"
        f"Welcome to MyApp! Your account has been created.\n"
        f"Email: {email}\n\n"
        f"Cheers,\nThe MyApp Team"
    )

    _send_email(email, subject, _html_card("Welcome to MyApp! 🎉", body_html), text_body)


# ─────────────────────────────────────────────────────────────────
#  2.  UPDATE EMAIL  –  triggered on update_user()
# ─────────────────────────────────────────────────────────────────
def send_update_email(name: str, email: str,age : int , old_name: str, old_email: str , old_age : int) -> None:
    subject = "✏️ Your account info was updated"

    body_html = f"""
        <p>Hi <strong>{name}</strong>,</p>
        <p>Your account details have just been updated. Here's a summary
           of what changed:</p>

        <!-- Two-column diff table -->
        <table width="100%" cellpadding="10" cellspacing="0"
               style="border-collapse:collapse;margin:20px 0;
                      border-radius:8px;overflow:hidden;font-size:14px;">
          <thead>
            <tr style="background:#4F46E5;color:#fff;">
              <th style="text-align:left;padding:10px 16px;">Field</th>
              <th style="text-align:left;padding:10px 16px;">Before</th>
              <th style="text-align:left;padding:10px 16px;">After</th>
            </tr>
          </thead>
          <tbody>
            <tr style="background:#f9fafb;">
              <td style="padding:10px 16px;border-bottom:1px solid #e5e7eb;">
                Name</td>
              <td style="padding:10px 16px;border-bottom:1px solid #e5e7eb;
                         color:#ef4444;">{old_name}</td>
              <td style="padding:10px 16px;border-bottom:1px solid #e5e7eb;
                         color:#22c55e;">{name}</td>
            </tr>
            <tr style="background:#ffffff;">
              <td style="padding:10px 16px;">Email</td>
              <td style="padding:10px 16px;color:#ef4444;">{old_email}</td>
              <td style="padding:10px 16px;color:#22c55e;">{email}</td>
              <td style="padding:10px 16px;color:#ef4444;">{old_age}</td>
              <td style="padding:10px 16px;color:#22c55e;">{age}</td>
            </tr>
          </tbody>
        </table>

        <p style="color:#6b7280;font-size:13px;">
          If you did <em>not</em> make this change, please contact support
          immediately.
        </p>
        <p>Thanks,<br><strong>The MyApp Team</strong></p>
    """

    text_body = (
        f"Hi {name},\n\n"
        f"Your account was updated.\n"
        f"Name : {old_name} → {name}\n"
        f"Email: {old_email} → {email}\n\n"
        f"If you didn't do this, contact support.\n\nThanks,\nThe MyApp Team"
    )

    _send_email(email, subject, _html_card("Account Updated ✏️", body_html), text_body)


# ─────────────────────────────────────────────────────────────────
#  3.  GOODBYE EMAIL  –  triggered on delete_user()
# ─────────────────────────────────────────────────────────────────
def send_goodbye_email(name: str, email: str) -> None:
    subject = "👋 We're sad to see you go"

    body_html = f"""
        <p>Hi <strong>{name}</strong>,</p>
        <p>Your account (<strong>{email}</strong>) has been
           <span style="color:#ef4444;font-weight:600;">permanently deleted</span>
           from our system.</p>

        <table cellpadding="0" cellspacing="0"
               style="margin:24px 0;background:#fff7ed;border-radius:8px;
                      border-left:4px solid #f97316;padding:16px 20px;
                      width:100%;">
          <tr>
            <td>
              <p style="margin:0;color:#92400e;font-size:14px;">
                All your data has been removed. This action cannot be undone.
              </p>
            </td>
          </tr>
        </table>

        <p>We'd love to know what we could have done better.
           Feel free to reply to this email with any feedback.</p>
        <p>We hope to see you again someday. 🙏<br>
           <strong>The MyApp Team</strong></p>
    """

    text_body = (
        f"Hi {name},\n\n"
        f"Your account ({email}) has been permanently deleted.\n"
        f"We're sorry to see you go. Feel free to reach out any time.\n\n"
        f"The MyApp Team"
    )

    _send_email(email, subject, _html_card("Goodbye 👋", body_html), text_body)
