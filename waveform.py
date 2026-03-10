import numpy as np
import sounddevice as sd

FS = 44100
UNIT = 0.1
THRESHOLD = 0.03

def audio_callback(indata, frames, time, status):
    # RMS of whole chunk
    volume_norm = np.linalg.norm(indata) / np.sqrt(len(indata))
    
    # Compare to threshold
    if volume_norm > THRESHOLD:
        # Detection
        print("█", end="", flush=True) 
    else:
        # Silence
        print(".", end="", flush=True)

def main():
    # Start listening
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=FS, blocksize=1024):
        print("Listening...")
        while True:
            sd.sleep(1000)


if __name__ == "__main__":
    main()