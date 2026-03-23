from morse import convert_text_to_morse
from waveform import listen
from beeps import beep_morse
from rich.prompt import Prompt

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