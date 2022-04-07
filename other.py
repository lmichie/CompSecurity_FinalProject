from tkinter import *
from tkinter.font import Font
from tkinter import messagebox


# Start Logic
letter2number = { '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                 '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18,
                 'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29,
                 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35, ' ': 36}

number2letter = { 0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
                 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I',
                 19: 'J', 20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T',
                 30: 'U', 31: 'V', 32: 'W', 33: 'X', 34: 'Y', 35: 'Z', 36: ' '}


#Takes the user's entry and converts it to numbers for easy modulizing
def convert_to_numbers(user_entry):
    modified = []
    for char in user_entry:
        modified.append(letter2number[char])
    return modified

#Once the message, in number form, has been encoded we revert to proper lettering
def convert_to_letters(entry):
    modified = ""
    for num in entry:
        modified += number2letter[num]
    return modified

#Takes key and duplicates or cuts off the key to make it match the length
#of the message
#EX: message: "hello world" with key: "test" turns key into "testtesttes"
def keylenghter(entry, key):
    new_key = ''
    while len(key) < len(entry):
        key = key + key
    new_key = key[:len(entry)]
    return new_key

#turns uncoded message in number form into encoded message in number form based on
#the logic described here: https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher#Algebraic_description
def encoder(entry, key):
    encoded = []
    for num in range(len(entry)):
        new_char = (entry[num] + key[num]) % len(letter2number)
        encoded.append(new_char)
    return encoded

#turns encoded message in number form into decoded message in number form based on
#the logic described here: https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher#Algebraic_description
def decoder(entry, key):
    decoded = []
    for num in range(len(entry)):
        new_char = (entry[num] - key[num]) % len(number2letter)
        decoded.append(new_char)
    return decoded


# End Logic
# Begin GUI

window = Tk()
window.title("Asker & Solver")
window.geometry('350x160')
myFont = Font(family="Fixedsys", size=9)

choice = IntVar()

message_label = Label(window, text="Message:", font=myFont)
message_label.grid(column=0, row=0)

message = Entry(window, width=30, font=myFont)
message.grid(column=1, row=0)

key_label = Label(window, text="Key:", font=myFont)
key_label.grid(column=0, row=1)

key = Entry(window, width=30, font=myFont)
key.grid(column=1, row=1)

result_label = Label(window, text="Your Result Will Appear Here", font=myFont)
result_label.grid(column=1, row=4)
def begin_encoding():
    given_message = message.get()
    given_key = key.get()

    if len(given_key) == 0:
        messagebox.showerror("Key Error", "Please Enter a Key")
        return

    given_message = given_message.upper()
    given_key = given_key.upper()
    long_key = keylenghter(given_message, given_key)

    try:
        number_message = convert_to_numbers(given_message)
    except:
        messagebox.showerror("Character Error","Only Alphanumeric characters and spaces are allowed in the message")
        result_label.configure(text="Error in Encoding")
        return

    try:
        number_key = convert_to_numbers(long_key)
    except:
        messagebox.showerror("Character Error","Only Alphanumeric characters and spaces are allowed in the key")
        result_label.configure(text="Error in Encoding")
        return

    encoded_numbers = encoder(number_message, number_key)
    encoded_message = convert_to_letters(encoded_numbers)
    encoded_message = '"' + encoded_message
    encoded_message = encoded_message + '"'
    result_label.configure(text=encoded_message)


def begin_decoding():
    given_message = message.get()
    given_key = key.get()
    if len(given_key) == 0:
        messagebox.showerror("Key Error", "Please Enter a Key")
        return

    given_message = given_message.upper()
    given_key = given_key.upper()
    long_key = keylenghter(given_message, given_key)
    try:
        number_message = convert_to_numbers(given_message)
    except:
        messagebox.showerror("Character Error","Only Alphanumeric characters and spaces are allowed in the message")
        result_label.configure(text="Error in Decoding")
        return
    try:
        number_key = convert_to_numbers(long_key)
    except:
        messagebox.showerror("Character Error","Only Alphanumeric characters and spaces are allowed in the key")
        result_label.configure(text="Error in Decoding")
        return

    decoded_numbers = decoder(number_message, number_key)
    decoded_message = convert_to_letters(decoded_numbers)
    decoded_message = '"' + decoded_message
    decoded_message = decoded_message + '"'
    result_label.configure(text=decoded_message)


to_encode = Button(window,text = "Encode",command=begin_encoding,font = myFont)
to_encode.grid(column=1, row=2)

to_decode = Button(window, text="Decode", command=begin_decoding, font=myFont)
to_decode.grid(column=1, row=3)


window.mainloop()

# End GUI
