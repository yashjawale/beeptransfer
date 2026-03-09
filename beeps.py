import sounddevice as sd
import numpy as np
import time

sample_rate = 44100
dot_duration = 0.1

def beep(type):
    
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