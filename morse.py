alpha_to_morse = {
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    " ": "WAIT"
}

morse_to_alpha = {value: key for key, value in alpha_to_morse.items()}


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