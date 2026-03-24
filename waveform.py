import numpy as np
import sounddevice as sd
import sys

from project import convert_morse_to_char

FS = 44100
UNIT = 0.1
THRESHOLD = 0.03

# keep track of high/low count & formed letter
high = 0
low = 0
letter = ""

is_detecting = False


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


def listen():
    # Start listening
    with sd.InputStream(
        callback=audio_callback, channels=1, samplerate=FS, blocksize=1024
    ):
        print("Listening...")
        while True:
            sd.sleep(1000)
