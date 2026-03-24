from rich.prompt import Prompt
import time
import numpy as np
import sounddevice as sd
import sys

from morse import ALPHA_TO_MORSE, MORSE_TO_ALPHA

# constants
SAMPLE_RATE = 44100
DOT_DURATION = 0.1
FS = 44100
UNIT = 0.1
THRESHOLD = 0.03


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
    for code in morse:
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


# entry point of program
def main():
    
    # print(sys.argv)
        
    # Prompt user to program modes
    choice = Prompt.ask("Choose mode of program", choices=["send", "listen"], default="send")
    
    
    if choice == "send":
        text = Prompt.ask("Enter your message")
        print("Beeping message...")
        morse = convert_text_to_morse(text)
        
        # append end signal
        morse.append("...---...")
        
        beep_morse(morse)
    
    if choice == "listen":
        listen()


if __name__ == "__main__":
    main()