import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional


class EmailService:
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str, use_tls: bool = True):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    def send_email(
        self,
        subject: str,
        body: str,
        from_email: str,
        to_emails: List[str],
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None,
        is_html: bool = False
    ) -> bool:
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = ", ".join(to_emails)
            msg['Subject'] = subject
            if cc_emails:
                msg['Cc'] = ", ".join(cc_emails)

            # Set body
            mime_type = 'html' if is_html else 'plain'
            msg.attach(MIMEText(body, mime_type))

            # Connect to SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)
                
                all_recipients = to_emails + (cc_emails if cc_emails else []) + (bcc_emails if bcc_emails else [])
                server.sendmail(from_email, all_recipients, msg.as_string())
            
            print("Email sent successfully.")
            return True

        except Exception as e:
            print(f"Failed to send email: {e}")
            return False


# Example usage
if __name__ == "__main__":
    email_service = EmailService(
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        username="nodes@zaiv.io",
        password="Z@1vio$0(nodes)",
    )

    email_service.send_email(
        subject="Test Email",
        body="<h1>Hello, this is a test email.</h1>",
        from_email="nodes@zaiv.io",
        to_emails=["hussain_ce47@yahoo.com"],
        is_html=True
    )
