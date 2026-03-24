from rich.prompt import Prompt
from rich.progress import track
import time
import numpy as np
import sounddevice as sd
import sys
import re

from morse import ALPHA_TO_MORSE, MORSE_TO_ALPHA

# constants
SAMPLE_RATE = 44100
DOT_DURATION = 0.1
FS = 44100
UNIT = 0.1
THRESHOLD = 0.03
END_SIGNAL = "...---..."

# keep track of high/low count & formed letter
high = 0
low = 0
letter = ""
is_detecting = False


# convert text to morse code
def convert_text_to_morse(text):
    converted = []
    for char in text.lower():
        if char in ALPHA_TO_MORSE:
            converted.append(ALPHA_TO_MORSE[char])
    
    return converted


# convert morse code to its corresponding character
def convert_morse_to_char(morse):
    if morse in MORSE_TO_ALPHA:
        return MORSE_TO_ALPHA[morse]
    return ""


# sends out a beep to speakers depending on whether WAIT/dot/dash
def beep(type):

    # After each word is complete
    if type == "WAIT":
        time.sleep(DOT_DURATION * 7)
        return

    duration = DOT_DURATION if type == "dot" else DOT_DURATION * 3

    # Generate numpy array for time duration
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)

    # Create beep sound as sine wave
    # Sine wave formule -> Amplitude * sin(2 * pi * frequency * time)
    beep = 0.5 * np.sin(2 * np.pi * 800 * t)

    # Play beep and wait for it to finish
    sd.play(beep, SAMPLE_RATE)
    sd.wait()

    # Silence for one dot duration
    time.sleep(DOT_DURATION)


# beeps out morse code based on input
def beep_morse(morse):
    for code in track(morse, description="Sending message..."):
        if code == "WAIT":
            beep("WAIT")
        else:
            for char in code:
                if char == ".":
                    beep("dot")
                elif char == "-":
                    beep("dash")

            # Sleep between letters
            time.sleep(DOT_DURATION * 3)


# passed on as callback for recording
# prints out decoded message as recorded
def audio_callback(indata, frames, time, status):
    # RMS of whole chunk
    volume_norm = np.linalg.norm(indata) / np.sqrt(len(indata))

    global high, low, letter, message, is_detecting

    # Compare to threshold
    if volume_norm > THRESHOLD:
        # Detection

        # begin detection after first high signal
        if not is_detecting:
            is_detecting = True

        # word complete
        if 47 <= low <= 55:
            print(convert_morse_to_char(letter), end="", flush=True)
            letter=""
            
            # space after each word
            print(" ", end="", flush=True)

        # letter complete
        if 16 <= low <= 22:
            print(convert_morse_to_char(letter), end="", flush=True)
            letter = ""

        high += 1
        low = 0

    else:
        # Silence

        if is_detecting:
            # register dash
            if 12 <= high <= 13:
                letter += "-"

            # register dot
            if 3 <= high <= 5:
                letter += "."

            low += 1
            high = 0
    
    if letter == "...---...":
        print("----------------")
        print("COMPLETE")
        sys.exit()


# triggeres sounddevice listening
def listen():
    # Start listening
    with sd.InputStream(
        callback=audio_callback, channels=1, samplerate=FS, blocksize=1024
    ):
        print("Listening...")
        while True:
            sd.sleep(1000)


# filters message with only alphabets & numbers
def filter_message(message):
    return re.sub(r"[^a-zA-Z0-9 ]", "", message).lower()


# entry point of program
def main():
    
    arg_length = len(sys.argv)
    
    mode = ""
    message = ""
    
    # if --listen supplied
    if arg_length == 2 and sys.argv[1] == "--listen":
        mode = "listen"
    
    # if --send supplied
    if arg_length == 3 and sys.argv[1] == "--send":
        mode = "send"
        message = filter_message(sys.argv[2])
    
    if arg_length > 1 and not (mode == "listen" or (mode == "send" and message)):
        print("Invalid arguments")
        sys.exit(1)
    
    
    # Prompt user to program modes if flag not provided
    if arg_length == 1:
        mode = Prompt.ask("Choose mode of program", choices=["send", "listen"], default="send")
    
    
    if mode == "send":
        text = message or Prompt.ask("Enter your message")
        print("Encoding message...")
        morse = convert_text_to_morse(text)
        
        # append end signal
        morse.append(END_SIGNAL)
        
        beep_morse(morse)
    
    if mode == "listen":
        listen()


if __name__ == "__main__":
    main()