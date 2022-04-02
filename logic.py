# # imports

# # caesars' cipher function

# # encryption

# def encryption(message, shifter_key):
#     encryption_result = ""

#     # go through every character
#     for i in range(len(message)):
#         letter = message[i]

#         if (letter.isupper()):
#             encryption_result += chr((ord(letter) + shifter_key - 65)%26 +65)
#         else:
#             encryption_result += chr((ord(letter) + shifter_key - 97)%26 +97)
    
#     return encryption_result

# # move the text


# def encrypt_rot13(message, key=13):
#     encryption_result = ""

#     for i in range(len(message)):
#         letter = message[i]
#         if (letter.isalpha()):
#             if (letter.isupper()):
#                 encryption_result += chr((ord(letter) - key - 65)%26 +65)
#             elif (letter.islower()):
#                 encryption_result += chr((ord(letter) - key - 97)%26 +97)
#         elif (letter.isnumeric()):
#             encryption_result += letter
#         elif (letter == " "):
#             encryption_result += letter
#         else:
#             if (letter == "."):
#                 encryption_result += letter 
#     return encryption_result

# print(encrypt_rot13("o"))


# import tkinter
# from tkinter import ttk 

# main_window = tkinter.Tk()

# main_window.geometry("800x800")

# new_combo_box = ttk.Combobox(values = [
#     "David",
#     "Alex"
# ])
# new_combo_box.grid(row = 0, column = 0)
# new_combo_box.current(1)

# def get_combo_value():
#     the_value = new_combo_box.get()
#     return the_value

# selected = get_combo_value()

# execute_button = tkinter.Button(text = "select", command = get_combo_value)
# execute_button.grid(row = 1, column = 0)

# change_label = tkinter.Label(text = selected)
# change_label.grid(row = 2, column = 0)
# change_label.update()

# print(selected)

# main_window.mainloop()


# vigenere cipher

"""
alphabet = a b c d e f g h 
keys     = 1 2 3 4 5 6 7 9 

keyword = "bad" 
           214
plain_text        =     "adefhcba"
                         badbadba
shift_by                 21421421
encrypted_message =      ceihigdb

"""
from string import ascii_letters

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
def check_alphabet_position(letter):
    alphabet_postion = sorted_dictionary[letter]
    return alphabet_postion

# this rotates the letters
def rotate(letter, rotate_value):
    if letter.isupper():
        shift_value = 65
    if letter.islower():
        shift_value = 97
    
    return chr((ord(letter) + rotate_value - shift_value)%26 + shift_value)

# encryption function
def vigenere_encryption(message, key):
    encrypted_message = []
    starting_index = 0
    for letter in message:
        # checking if the letter is alpha
        rotation = check_alphabet_position(key[starting_index])
        # check if letter is not alpha
        if not letter in sorted_dictionary:
            encrypted_message.append(letter)
        elif letter.isalpha():
            encrypted_message.append(rotate(letter, rotation))
        
        # checking if keyword has reached the end
        if starting_index == (len(key) -1):
            starting_index = 0
        else:
            starting_index += 1
    
    return "".join(encrypted_message)

new_message = "Hey"
new_key = "david"

print(vigenere_encryption(new_message, new_key))
