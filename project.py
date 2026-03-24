from morse import alpha_to_morse, morse_to_alpha
from waveform import listen
from rich.prompt import Prompt
import time
import numpy as np
import sounddevice as sd


sample_rate = 44100
dot_duration = 0.1


def convert_text_to_morse(text):
    converted = []
    for char in text.lower():
        if char in alpha_to_morse:
            converted.append(alpha_to_morse[char])
    
    return converted


def convert_morse_to_char(morse):
    if morse in morse_to_alpha:
        return morse_to_alpha[morse]
    return ""


def beep(type):

    # After each word is complete
    if type == "WAIT":
        time.sleep(dot_duration * 7)
        return

    duration = dot_duration if type == "dot" else dot_duration * 3

    # Generate numpy array for time duration
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # Create beep sound as sine wave
    # Sine wave formule -> Amplitude * sin(2 * pi * frequency * time)
    beep = 0.5 * np.sin(2 * np.pi * 800 * t)

    # Play beep and wait for it to finish
    sd.play(beep, sample_rate)
    sd.wait()

    # Silence for one dot duration
    time.sleep(dot_duration)

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
            time.sleep(dot_duration * 3)


def main():
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