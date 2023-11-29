import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def send_email(to_email: str, subject: str, message: str):
    # todo remake this email and password so they will be setting from .env file
    from_email = "asdasdasd"  # Replace with your email address
    password = "asdasdasd"  # Replace with your email password

    try:
        server = smtplib.SMTP("smtp.mail.ru", 587)
        server.starttls()
        server.login(from_email, password)

        # Create the email message
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = formataddr(("Your Name", from_email))
        msg['To'] = to_email

        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        return {"message": "Email sent successfully"}
    except Exception as e:
        return {"message": f"Failed to send email: {str(e)}"}


# print(send_email(to_email='malysh_mikhail_s@mail.ru', subject='123', message='234'))
