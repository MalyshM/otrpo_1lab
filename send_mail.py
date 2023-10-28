import smtplib


def send_email(to_email: str, subject: str, message: str):
    from_email = "asdsadasdasdasd"  # Replace with your email address
    password = "asdasdasdasdasd"  # Replace with your email password

    try:
        server = smtplib.SMTP("smtp.mail.ru", 587)
        server.starttls()
        server.login(from_email, password)

        email_body = f"Subject: {subject}\n\n{message}"
        server.sendmail(from_email, to_email, email_body)
        server.quit()

        return {"message": "Email sent successfully"}
    except Exception as e:
        return {"message": f"Failed to send email: {str(e)}"}


# print(send_email(to_email='malysh_mikhail_s@mail.ru', subject='123', message='234'))
