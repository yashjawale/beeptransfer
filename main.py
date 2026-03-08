from morse import morse_code
from beeps import beep

def main():
    print(morse_code["a"])
    beep("dash")
    beep("dot")
    beep("dot")
    beep("dash")


if __name__ == "__main__":
    main()