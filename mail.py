import smtplib, ssl #importing smtplib and ssl for sending mails
from email.mime.text import MIMEText #importing from mime for sending mails
from email.mime.multipart import MIMEMultipart #importing from mime for sending mails


def email(list1,list2):#function to send an email
    sender_email ='pythoncrm123@gmail.com'
    receiver_email =list1
    str2=str(list2)
    password = 'jtrqxdmdevhyqmui'

    message = MIMEMultipart("alternative")
    message["Subject"] = input('Please enter the subject of the mail: ')


    text =input('Please enter the context of the mail: ')
    final_text=(text+'\n'+str2)
    part1 = MIMEText(final_text, "plain")
    
    message.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
