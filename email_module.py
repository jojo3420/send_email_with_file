import os
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
# from email.utils import COMMASPACE, formatdate
from email.utils import formatdate
from email import encoders
from dotenv import load_dotenv

load_dotenv('.env')


def send_mail(send_from: str, send_to: str, subject: str, message: str,
              files=[],
              server="smtp.gmail.com",
              port=587,
              username=os.getenv('EMAIL_CLIENT_USERNAME'),
              password=os.getenv('EMAIL_CLIENT_PWD'),
              use_tls=True
              ):
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (list[str]): to name(s)
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename={}'.format(Path(path).name))
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()


if __name__ == '__main__':
    send_mail(
        send_from='spring3420@daum.net',
        send_to='jjjhhhvvv@naver.com',
        subject='title',
        message="hello?",
        files=['./msg.txt']
    )
