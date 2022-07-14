import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import datetime
import random
import pandas as pd


sender_email = "test3@gmail.com"
password = "xgvpajkworonzghx"

now = datetime.datetime.now()
now_tuple = (now.month, now.day)


data = pd.read_csv("birthdays.csv")
print(data)
birthday_dict = {(data_row.month, data_row.day): data_row for (index, data_row) in data.iterrows()}


if now_tuple in birthday_dict:
    birthday_person = birthday_dict[now_tuple]
    file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[NAME]", birthday_person["name"])
    # initialise message instance
    msg = MIMEMultipart()
    msg["Subject"] = "Happy Birthday, LOVE"
    msg["From"] = sender_email
    msg['To'] = birthday_person["email"]

    text = """\
    """

    body_text = MIMEText(text, 'plain')  #
    msg.attach(body_text)  # attaching the text body into msg

    html = """\
    <html>
      <body>
        <p>{}</p>
      </body>
    </html>
    """
    body_html = MIMEText(html.format(contents), 'html')  # parse values into html text
    msg.attach(body_html)  # attaching the text body into msg

    ## Image
    img_name = 'minions-party-einladungen.jpg'
    with open(img_name, 'rb') as fp:
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename=img_name)
        msg.attach(img)

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user="mo.alaa40123@gmail.com", password=password)
        connection.sendmail(to_addrs=birthday_person['email'], from_addr=sender_email, msg=msg.as_string())
