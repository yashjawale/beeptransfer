from morse import convert_text_to_morse, convert_morse_to_char
from beeps import beep_morse

def main():
    
    morse = convert_text_to_morse("This is Cs50")
    beep_morse(morse)


if __name__ == "__main__":
    main()