# imports
import tkinter
from tkinter import ttk
from string import ascii_letters

# main class 

class MainWindow(tkinter.Tk):
    """ This is the main window, a child class of tkinter """
    def __init__(self):
        super().__init__()
        """ The main window properties """
        # main window title
        self.title("Cryptographic Ciphers")
        # main window size
        self.geometry("1320x420")
        # main window color
        self.configure(background = "light blue")


    pattern = {}
    dictionary = pattern.fromkeys(ascii_letters)
    sorted_dictionary = {}

    # assigning values 
    counter = 0
    counter2 = 0
    for key, value in dictionary.items():
        if counter <= 25:
            value = counter
            counter += 1
            sorted_dictionary[key] = value
        else:
            value = counter2
            counter2 += 1
            sorted_dictionary[key] = value

    # print(sorted_dictionary)

    # check the alphabet position
    def check_alphabet_position(self, letter):
        alphabet_postion = self.sorted_dictionary[letter]
        return alphabet_postion

    # this rotates the letters
    def rotate(self, letter, rotate_value):
        if letter.isupper():
            shift_value = 65
        if letter.islower():
            shift_value = 97
        
        return chr((ord(letter) + rotate_value - shift_value)%26 + shift_value)

    # encryption function
    def vigenere_encryption(self, message, key):
        encrypted_message = []
        starting_index = 0
        for letter in message:
            # checking if the letter is alpha
            rotation = self.check_alphabet_position(key[starting_index])
            # check if letter is not alpha
            if not letter in self.sorted_dictionary:
                encrypted_message.append(letter)
            elif letter.isalpha():
                encrypted_message.append(self.rotate(letter, rotation))
            
            # checking if keyword has reached the end
            if starting_index == (len(key) -1):
                starting_index = 0
            else:
                starting_index += 1
        
        return "".join(encrypted_message)


root_window = MainWindow()

if __name__ == "__main__":
    root_window.mainloop()
