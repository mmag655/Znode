import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional

def get_formatted_transfer_email(username, total_token, link, tx_hash, wallet_address):
    body = f"""
    <html>
    <body>
        <p>Hi {username},</p>

        <p>Your {total_token} token has been redeemed successfully.</p>

        <p>Explorer link: <a href="{link}" target="_blank">{link}</a></p>
        <p>Transaction hash: {tx_hash}</p>

        <p>Tokens have been sent to your contract address: {wallet_address}</p>

        <p>If you have any questions or face issues logging in, reach out to Mike directly at 
        <a href="mailto:mike@zaivio.com">mike@zaivio.com</a> so he can confirm your information.</p>

        <p>Thank you!<br><strong>Team ZAIVIO</strong></p>
    </body>
    </html>
    """
    return body

def get_formatted_fail_email(username, total_token, wallet_address):
    body = f"""
    <html>
    <body>
        <p>Hi {username},</p>

        <p>Your {total_token} token redemption has failed.</p>

        <p>Tokens could not be sent to your contract address: {wallet_address}</p>

        <p>Please reach out to Mike directly at 
        <a href="mailto:mike@zaivio.com">mike@zaivio.com</a> so he can address your issue.</p>

        <p>Thank you!<br><strong>Team ZAIVIO</strong></p>
    </body>
    </html>
    """
    return body



def get_zaivio_welcome_email(name: str, password: str) -> str:
    temp_password = f"{password}"

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <p>Hi {name},</p>

        <p>Welcome to the <strong>ZAIVIO Nodes Dashboard</strong>.</p>

        <ul>
            <li>Go to the URL: <a href="https://zaivionodes.com/dashboard">https://zaivionodes.com/dashboard</a></li>
            <li>Sign in using your email address</li>
            <li>Your temporary password is: <strong>{temp_password}</strong></li>
        </ul>

        <p><em>(So if your name is John, it would be JohXrbnh@123)</em></p>

        <p>After you log in, you will be automatically redirected to the change password page.</p>

        <p>If you have any questions or face issues logging in, reach out to Mike directly at 
        <a href="mailto:mike@zaivio.com">mike@zaivio.com</a> so he can confirm your information.</p>

        <p>Thank you!<br><strong>Team ZAIVIO</strong></p>
    </body>
    </html>
    """
    return html_body


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

def get_mail_service(username="nodes@zaiv.io"):
    
    service = EmailService(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    username=username,
    password="kjny atyw cyav mpje"
    )
    return service

def send_bulk_emails(email_service):
    # List of (Name, Email) tuples
    recipients = [
        ("Mike Magolnick", "Mike@magolnick.com"),
        # ("Greg Nesspor", "Nessporag@verizon.net"),
        # ("Adam Moeller", "Moeller1248@gmail.com"),
        # ("Pam Bahler", "Pam@weblopez.com"),
        # ("Carolyn Stewart", "Carolyn@peaksappraisal.com"),
        # ("Kevin Towey", "Toweyk@gmail.com"),
        # ("Edwin Romero", "Edromer20@gmail.com"),
        # ("Jeff Perkins", "Jalaperkins4@outlook.com"),
        # ("Cory Reynolds", "Cnibl@proton.me"),
        # ("Clint Jensen", "Clint.jensen@gmail.com"),
        # ("Ryan Hamar", "Ryan.hamar@gmail.com"),
        # ("Todd Martin", "Admin@masterconcepts.biz"),
        # ("John Skates", "John.skates@gmail.com"),
        # ("Mark Ross", "Markrosswinning@gmail.com"),
        # ("Shawn Luetje", "Divineprovidence.shawn@gmail.com"),
        # ("Jeremy Reeves", "Jreevespersonal@protonmail.com"),
        # ("Grant Bomsta", "Grantbomsta@gmail.com"),
        # ("Ryan Farmer", "Ryanlfarmer@gmail.com"),
        # ("Jerry Rutkey", "jgrutkey@gmail.com"),
        # ("Mark Ambrosius", "Markandcj1@gmail.com"),
        # ("Theron Hatch", "Thecryptoron@proton.me"),
        # ("Al Rosenblum", "Aladvancingwithus@gmail.com"),
        # ("Matthew Powell", "Matthew6195@gmail.com"),
        # ("Adam Price", "Adammprice@hotmail.com"),
        # ("James Hudson", "Jmshudson@msn.com"),
        # ("Jack Allen", "2015aero.mail@gmail.com"),
        # ("Don Juvet", "Djsparent25@gmail.com"),
        # ("Chad Moeller", "Chadmoeller99@gmail.com"),
        # ("Matthew Murphy", "Murphy43092@gmail.com"),
        # ("Patrick Binkowski", "Patrikbinkowski@protonmail.com"),
        # ("Randy Bartilson", "Ecmocrypto@gmail.com"),
        # ("Garret Biss", "Garret.biss@gmail.com"),
        # ("Leroy Trout", "Leroytrought@gmail.com"),
        # ("Michael Kohn", "mickyk7117@gmail.com"),
        # ('Hussain Muhammad', "hussain_ce47@yahoo.com"),
    ]

    for name, email in recipients:
        username = name.split()[0]
        try:
            email_service.send_email(
                subject="Welcome to ZAIVIO Nodes",
                body=get_zaivio_welcome_email(username,  f"{name[:3]}Xrbnh@123"),
                from_email="nodes@zaiv.io",
                to_emails=[email],
                is_html=True
            )
            print(f"Sent to {email}")
        except Exception as e:
            print(f"Failed to send to {email}: {e}")

# Example usage
if __name__ == "__main__":
    # email_service = EmailService(
    #     smtp_server="smtp.gmail.com",
    #     smtp_port=587,
    #     username="nodes@zaiv.io",
    #     # password="Z@1vio$0(nodes)",
    #     password="kjny atyw cyav mpje"
    # )
    # email_service = get_mail_service()

    # email_service.send_email(
    #     subject="Welcome to ZAIVIO Nodes",
    #     body=get_zaivio_welcome_email("Hussain"),
    #     from_email="nodes@zaiv.io",
    #     to_emails=["hussain_ce47@yahoo.com"],
    #     is_html=True
    # )
    email_service = get_mail_service()
    send_bulk_emails(email_service)