# -*- coding: utf-8 -*-
"""
@author: libor_komanek
"""

import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from string import ascii_uppercase, digits
from unidecode import unidecode
import math

qtCreatorFile = "AffineCipher.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

ALPHABET: str = ascii_uppercase + digits
MOD: int = len(ALPHABET)
L2N: dict = dict(zip(ALPHABET, range(MOD)))  # map letters to numbers
N2L: dict = dict(zip(range(MOD), ALPHABET))  # map numbers to letters
SPACE_REPRESENTATION: str = "XMEZERAX"


def filterText(text: str) -> str:
    """
    Returns a filtered string. Converts characters in string to uppercase unicode, removes special characters
    and replaces spaces with their string representation.
    :param text: raw text input
    :return: filtered string
    """
    text: str = unidecode(text).upper()
    result: str = ""
    for character in text:
        if character.isalnum():
            result += character
        elif character == " ":
            result += SPACE_REPRESENTATION
    return result


def getInverseA(a: int) -> int:
    """
    Returns inverse value of the original value or -1 if the inverse value does not exist.
    :param a: original value
    :return: inverse value or -1 if the value does not exist
    """
    if math.gcd(a, MOD) != 1:
        return -1
    else:
        for i in range(MOD):
            if(i * a % MOD) == 1:
                return i


def groupCharacters(text: str, n: int) -> str:
    """
    Returns the original string with spaces between groups of N characters.
    :param text: original string
    :param n: number of characters in every group
    :return: original string with grouped characters
    """
    result: str = ' '.join([
        text[i:i + n] for i in range(0, len(text), n)
    ])
    return result


def encipher(a: int, b: int, plain_text: str) -> str:
    """
    Returns cipher text created using the affine cipher. The resulting string has characters separated by a space
    after every 5th character.
    :param a: value of key a, must be co prime with mod (length of the used alphabet)
    :param b: value of key b
    :param plain_text: original text to be enciphered
    :return: cipher text
    """
    plain_text = filterText(plain_text)
    print(f"Filtered text:\n{plain_text}")
    if getInverseA(a) == -1:  # additional check for valid value
        raise ValueError("a must be co prime with mod")

    print("Enciphering...")
    cipher_text: str = ""
    for character in plain_text:
        cipher_text += N2L[(L2N[character] * a + b) % MOD]

    print(f"Raw cipher text:\n{cipher_text}")
    cipher_text = groupCharacters(cipher_text, 5)
    print(f"Formatted cipher text:\n{cipher_text}")
    return cipher_text


def decipher(a: int, b: int, cipher_text: str) -> str:
    """
    Returns deciphered text using the affine cipher.
    :param a: value of key a, must be co prime with mod (length of the used alphabet)
    :param b: value of key b
    :param cipher_text: text to be deciphered
    :return: plain text with the original message
    """
    cipher_text = cipher_text.replace(" ", "")
    print(f"Cipher text input:\n{cipher_text}")

    print("Deciphering...")
    plain_text = ""
    inverse_a = getInverseA(a)
    if inverse_a == -1:  # additional check for valid value
        raise ValueError("a must be co prime with mod")
    for character in cipher_text:
        plain_text += N2L[(inverse_a * (L2N[character] - b)) % MOD]

    plain_text = plain_text.replace("XMEZERAX", " ")
    print(f"Deciphered text:\n{plain_text}\n")
    return plain_text


class AffineCipher(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Affine cipher")
        self.fillAKeyComboBox()
        self.execute_button.clicked.connect(self.execute)

    def execute(self):
        """
        Checks user input from GUI and calls appropriate function.
        :return: 1 if successful; None if operation could not be executed
        """
        try:
            a: int = int(self.key_a.currentText())
            b: int = self.key_b.value()
            text: str = self.text_field.toPlainText()
            if len(text) < 1:
                raise ValueError("Text field cannot be empty!")
            print(f"\na = {a}; b = {b}; mod = {MOD}")
            print(f"Alphabet:\n{ALPHABET}")
            print(f"Cipher alphabet:\n{''.join([N2L[(L2N[c] * a + b) % MOD] for c in ALPHABET])}")
            if self.encipher_radio.isChecked():
                cipher_text: str = encipher(a, b, text)
                self.result_field.setPlainText(cipher_text)
            else:
                plain_text: str = decipher(a, b, text)
                self.result_field.setPlainText(plain_text)
        except Exception as e:
            self.result_field.setPlainText(f"Something went wrong! {str(e)}")

    def fillAKeyComboBox(self):
        """
        Fills a_key combo box with valid numbers which are co prime with mod.
        """
        for num in range(MOD):
            if math.gcd(num, MOD) == 1:
                self.key_a.addItem(str(num))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AffineCipher()
    window.show()
    sys.exit(app.exec())
