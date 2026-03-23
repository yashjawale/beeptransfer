import numpy as np
import sounddevice as sd

FS = 44100
UNIT = 0.1
THRESHOLD = 0.03

# keep track of high & low
high = 0
low = 0

letter = ""

flag = False


def audio_callback(indata, frames, time, status):
    # RMS of whole chunk
    volume_norm = np.linalg.norm(indata) / np.sqrt(len(indata))

    global high, low, letter, message, flag

    # Compare to threshold
    if volume_norm > THRESHOLD:
        # Detection
        # print(low, end=" ", flush=True)
        # print("█", end="", flush=True)

        if not flag:
            flag = True

        # word complete
        if 47 <= low <= 55:
            # print("END", end=" ", flush=True)
            print(letter)
            letter=""
            print("WAIT", flush=True)

        # letter complete
        if 16 <= low <= 22:
            # print("END", end=" ", flush=True)
            print(letter)
            letter = ""

        high += 1
        low = 0

    else:
        # Silence
        # print(".", end="", flush=True)

        if flag:
            # register dash
            if 12 <= high <= 13:
                letter += "-"
                print("DASH", end=" ", flush=True)

            # register dot
            if 3 <= high <= 5:
                letter += "."
                print("DOT", end=" ", flush=True)

            low += 1
            high = 0


def main():
    # Start listening
    with sd.InputStream(
        callback=audio_callback, channels=1, samplerate=FS, blocksize=1024
    ):
        print("Listening...")
        while True:
            # print(flag, high, low, letter, message)
            sd.sleep(1000)


if __name__ == "__main__":
    main()
