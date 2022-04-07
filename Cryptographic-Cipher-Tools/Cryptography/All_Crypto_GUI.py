from tkinter import *
import random
from tkinter.font import BOLD
import webbrowser
from tkinter import ttk
from time import strftime
from PIL import Image, ImageTk
from ciphers import caesarC, railfenceC, columnerC,vignereC


root = Tk()
root.configure(background="#3FBE7F")
root.title("cryptociphers")
title_frame = Frame(root, width=180, height=180, relief=SUNKEN, borderwidth=10)
title_frame.pack()


img=Image.open('Images/crypto1.jpg')
img=ImageTk.PhotoImage(img)
icon=Button(title_frame,image=img)
icon.pack()

################################################################################################################################
def cipher():
    root.destroy()

    window = Tk()

    window.configure(background='gray')
    window.title("Cryptographic ciphers")


    left_frame = Frame(window, width=200, height=600, relief=SUNKEN)
    left_frame.pack(side=LEFT)

    main_frame = Frame(window, width=800, height=100, relief=SUNKEN, borderwidth=10)
    main_frame.pack()

    main = Frame(window, width=800, height=400, relief=SUNKEN, bg='#BF4340')
    main.pack()

    time_frame = Frame(window, width=500, height=30, relief=SUNKEN, background='gray')
    time_frame.pack(side=BOTTOM)

    ###############################################################################################################################

    def remove():
        for widget in main.winfo_children():
            widget.destroy()

    def window_show():
        remove()

    def lab():

        text_label = Label(main, text="Enter text: ", font=('fixedsys', 16, "bold"), bg="tomato", fg="white")
        text_label.grid(row=0, column=0, padx=20, pady=20)

        scroll_text = ttk.Scrollbar(main, orient=VERTICAL)
        text_box = Text(main, height=8, width=40, pady=10, yscrollcommand=scroll_text.set, bg='white')
        text_box.grid(row=1, column=0, pady=1, padx=1)
        scroll_text.config(command=text_box.yview)
        scroll_text.grid(row=1, column=1, sticky='NS')

        key_label = Label(main, text="Enter key: ", font=('fixedsys', 14), pady=15,
                          bg='black', fg="cyan")
        key_label.grid(row=2, column=0)

        scroll_text2 = ttk.Scrollbar(main, orient=VERTICAL)
        new_text = Text(main, height=8, width=40, pady=10, yscrollcommand=scroll_text2.set, bg='white')
        new_text.grid(row=1, column=2, columnspan=2, padx=(10, 0))
        scroll_text2.config(command=new_text.yview)
        scroll_text2.grid(row=1, column=4, sticky='NS')
        return text_box, new_text

    ################################################################################################################################
    def caesar_cipher():  # 1st cipher

        remove()


        list_key = ttk.Combobox(main)
        list_key['values'] = (
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26)
        list_key.current(0)
        list_key.grid(row=5, column=0)

        text_box, new_text = lab()
        sample = ""
        new_text.insert(1.0, sample)
        label = Label(main, text="caesar_cipher" , font=('Times New Roman', 16, "bold"),bg="#FDA73F")
        label.grid(row=0, column=1)

        def encrypt():
            new_text.delete('1.0', END)
            txt = text_box.get("1.0", END)
            key = int(list_key.get())
            enc_text = caesarC.encryption(txt, key)
            new_text.insert(1.0, enc_text)

        enc = Button(main, text="Encrypt", bd=10, width=10, command=encrypt,bg='#3FBE7F', fg='white')
        enc.grid(row=0, column=2, padx=20, pady=30)
        def decrypt():
            new_text.delete('1.0', END)
            txt = text_box.get("1.0", END)
            key = int(list_key.get())
            dec_text = caesarC.decryption(txt, key)
            new_text.insert(1.0, dec_text)

        dec = Button(main, text="Decrypt", bd=10, width=10, command=decrypt,bg='tomato2', fg='white')
        dec.grid(row=0, column=3, padx=10, pady=10)

    #############################################################################################################################


    ##############################################################################################################################
    def vignere_cipher():
        remove()

        key_text = Entry(main, width=40)
        key_text.grid(row=3, column=0, padx=10, pady=10)

        text_box, new_text = lab()
        sample = " "
        new_text.insert(1.0, sample)
        label = Label(main, text="vignere_cipher")
        label.grid(row=0, column=1)

        def encrypt():
            new_text.delete('1.0', END)
            txt = text_box.get("1.0", END)
            key = key_text.get()
            enc_text = vignereC.encrypt(txt, key)
            new_text.insert(1.0, enc_text)

        enc = Button(main, text="Encrypt", bd=10, width=10, command=encrypt,
                     bg='#3FBE7F', fg='white')
        enc.grid(row=0, column=2, padx=20, pady=30)

        def decrypt():
            new_text.delete('1.0', END)
            txt = text_box.get("1.0", END)
            key = key_text.get()
            dec_text = vignereC.decrypt(txt, key)
            new_text.insert(1.0, dec_text)

        dec = Button(main, text="Decrypt", bd=10, width=10, command=decrypt,
                     bg='tomato2', fg='white')
        dec.grid(row=0, column=3, padx=10, pady=10)

    #############################################################################################################################

    ################################################################################################################################

    def railfence_cipher():
        remove()

        list_key = ttk.Combobox(main)
        list_key['values'] = (2, 3, 4, 5, 6, 7, 8)
        list_key.current(0)
        list_key.grid(row=5, column=0)

        text_box, new_text = lab()
        sample = " "
        new_text.insert(1.0, sample)
        label = Label(main, text="railfence_cipher")
        label.grid(row=0, column=1)

        def encrypt():
            new_text.delete('1.0', END)
            string = (text_box.get("1.0", END)).strip()
            key = int(list_key.get())
            enc_text = railfenceC.encrypt(string, key)
            new_text.insert(1.0, enc_text)

        enc = Button(main, text="Encrypt", bd=10, width=10, command=encrypt,bg='#3FBE7F', fg='white')
        enc.grid(row=0, column=2, padx=20, pady=30)

        def decrypt():
            new_text.delete('1.0', END)
            string = (text_box.get("1.0", END)).strip()
            key = int(list_key.get())
            dec_text = railfenceC.decrypt(string, key)
            new_text.insert(1.0, dec_text)

        dec = Button(main, text="Decrypt", bd=10, width=10, command=decrypt,
                     bg='tomato2', fg='white')
        dec.grid(row=0, column=3, padx=10, pady=10)

    ###############################################################################################################################


    ############################################################################################################################
    def columnar_trans_cipher():
        remove()

        key_text = Entry(main, width=40)
        key_text.grid(row=3, column=0, padx=10, pady=10)

        text_box, new_text = lab()
        sample = " "
        new_text.insert(1.0, sample)
        label = Label(main, text="columnar_trans_cipher")
        label.grid(row=0, column=1)

        def encrypt():
            new_text.delete('1.0', END)
            txt = text_box.get("1.0", END)
            key = key_text.get().lower()
            enc_text = columnerC.encrypt(txt, key)
            new_text.insert(1.0, enc_text)

        enc = Button(main, text="Encrypt", bd=10, width=10, command=encrypt,bg='#3FBE7F', fg='white')
        enc.grid(row=0, column=2, padx=20, pady=30)

        def decrypt():
            new_text.delete('1.0', END)
            txt = text_box.get("1.0", END)
            key = key_text.get().lower()
            dec_text = columnerC.decrypt(txt, key)
            new_text.insert(1.0, dec_text)

        dec = Button(main, text="Decrypt", bd=10, width=10, command=decrypt,
                     bg='tomato2', fg='white')
        dec.grid(row=0, column=3, padx=10, pady=10)

    ###########################################################################################################################
    # buttons on window left lide
    home_button = Button(left_frame, padx=20, bd=10, text='Home', width=20, height=3, command=window_show,
                         bg='#FDA73F', fg='white', activebackground='black', font=('arial', 16, 'bold'),
                         activeforeground='#3FBE4F')
    home_button.grid(row=0, column=0)

    caesar = Button(left_frame, padx=20, bd=10, text='Caesar Cipher', width=20, height=3, command=caesar_cipher,
                    bg='white', fg='red', activebackground='black', font=('arial', 16, 'bold'),
                    activeforeground='#3FBE4F')
    caesar.grid(row=1, column=0)


    vignere = Button(left_frame, padx=20, bd=10, text='Vignere Cipher', width=20, height=3, command=vignere_cipher,
                     bg='white', fg='red', activebackground='black', font=('arial', 16, 'bold'),
                     activeforeground='#3FBE4F')
    vignere.grid(row=2, column=0)



    railfence = Button(left_frame, padx=20, bd=10, text='Railfence Cipher', width=20, height=3,
                       command=railfence_cipher, bg='white', fg='red', activebackground='black',
                       font=('arial', 16, 'bold'), activeforeground='#3FBE4F')
    railfence.grid(row=3, column=0)





    columnar = Button(left_frame, padx=20, bd=10, text='Columnar Transposition Cipher', width=26, height=3,
                      command=columnar_trans_cipher, bg='white', fg='red', font=('arial', 12, 'bold'),
                      activebackground='black', activeforeground='SeaGreen1')
    columnar.grid(row=4, column=0)


    Exit = Button(left_frame, text="Exit", padx=20, bd=10, width=23,height=3, command=window.destroy, activebackground="red",
                  bg='#8E7360', fg="white", font=('arial', 12, 'bold'), activeforeground="green2")
    Exit.grid(row=15, column=0)

    window.mainloop()


Welcome_label = Label(root, text="Welcome to Cryptography ciphers", padx=10, pady=30, bg="light gray", fg="black",
                      font=("Helvetica", 20, "bold")).pack(pady=30)
chiper_button = Button(root, text="Cryprocypher", padx=20, bd=10, width=20, height=3, command=cipher, bg="lightgreen",
                       fg="darkblue", activebackground='black', activeforeground='SeaGreen1')
chiper_button.pack(pady=30)


root.mainloop()

