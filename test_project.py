from project import filter_message, convert_morse_to_char, convert_text_to_morse


def test_filter_message():

    # special characters
    assert filter_message("hello$%^&*world") == "helloworld"

    # also include underscores
    assert filter_message("hello_world") == "helloworld"

    # preserve spaces
    assert filter_message("hello world") == "hello world"


def test_convert_morse_to_char():
    # single character
    assert convert_morse_to_char("..-") == "u"

    # invalid characters
    assert convert_morse_to_char("...---...") == ""


def test_convert_text_to_morse():
    # single character
    assert convert_text_to_morse("h") == ["...."]

    # multiple characters
    assert convert_text_to_morse("hello") == ["....", ".", ".-..", ".-..", "---"]

    # mixed with invalid characters
    assert convert_text_to_morse("h@t") == ["....", "-"]
