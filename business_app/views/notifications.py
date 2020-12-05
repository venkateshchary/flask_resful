import smtplib, ssl

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "vchary78@gmail.com"
password = "12314124"

# Create a secure SSL context
context = ssl.create_default_context()


def send_email(receiver_email, msg):
    """
        receiver email
        msg

    """
    server = smtplib.SMTP(smtp_server, port)
    try:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        # TODO: Send email here
        message = """\
        Subject: Hi there

        Transaction {0}.""".format(msg)
        server.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        print(e)
    finally:
        server.quit()
