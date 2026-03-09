from morse import convert_text_to_morse, convert_morse_to_char
from beeps import beep

def main():
    print(convert_text_to_morse("hello world"))
    
    morse = convert_text_to_morse("hello world")
    for code in morse:
        print(convert_morse_to_char(code), end="")


if __name__ == "__main__":
    main()