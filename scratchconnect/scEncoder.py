"""
The scratchconnect Encoder File
"""
import string

ALL_CHARS = list(string.ascii_uppercase + string.ascii_lowercase +
                 string.digits + string.punctuation + ' ')


class Encoder:
    """
    DON'T USE THIS
    """

    def __init__(self):
        pass

    def encode(self, text):
        text = str(text)
        number = ""
        for i in range(0, len(text)):
            char = text[i]
            index = str(ALL_CHARS.index(char) + 1)
            if int(index) < 10:
                index = '0' + index
            number += index
        return number

    def decode(self, encoded_code):
        encoded_code = str(encoded_code)
        i = 0
        text = ""
        while i < int(len(encoded_code) - 1 / 2):
            index = int(encoded_code[i] + encoded_code[i + 1]) - 1
            text += ALL_CHARS[index]
            i += 2
        return text

    def encode_list(self, data):
        if type(data) != list:
            raise TypeError(
                "To encode a list, the data should be in list form. To encode a text use the encode() function")
        encoded = ""
        for i in data:
            encoded += f"{self.encode(i)}00"
        return encoded

    def decode_list(self, encoded_list_data):
        decoded = []
        i = 0
        text = ""
        while i < int(len(encoded_list_data) - 1 / 2):
            code = encoded_list_data[i] + encoded_list_data[i + 1]
            index = int(code) - 1
            if code == "00":
                decoded.append(text)
                text = ""
            else:
                text += ALL_CHARS[index]
            i += 2
        return decoded
