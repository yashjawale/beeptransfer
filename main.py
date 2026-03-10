from morse import convert_text_to_morse, convert_morse_to_char
from beeps import beep_morse
from rich.prompt import Prompt

def main():
    choice = Prompt.ask("Choose mode of program", choices=["send", "listen"], default="send")
    
    if choice == "send":
        text = Prompt.ask("Enter your message")
        print("Beeping message...")
        morse = convert_text_to_morse(text)
        
        beep_morse(morse)


if __name__ == "__main__":
    main()