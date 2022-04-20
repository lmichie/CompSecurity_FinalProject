from tkinter import *
import random
from tkinter.font import BOLD
import webbrowser
from tkinter import ttk
from time import strftime
from PIL import Image, ImageTk
from ciphers import rsaC, vignereC, aesC


root = Tk()
root.configure(background="#636966")
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

	window.configure(background='#636966')
	window.title("Cryptographic ciphers")


	left_frame = Frame(window, width=200, height=600, relief=SUNKEN)
	left_frame.pack(side=LEFT)

	main_frame = Frame(window, width=800, height=100, relief=SUNKEN, borderwidth=10)
	main_frame.pack()

	main = Frame(window, width=800, height=400, relief=SUNKEN, bg='#6c6a75')
	main.pack()

	time_frame = Frame(window, width=500, height=30, relief=SUNKEN, background='gray')
	time_frame.pack(side=BOTTOM)

	###############################################################################################################################

	def remove():
		for widget in main.winfo_children():
			widget.destroy()

	def lab():
		text_label = Label(main, text="Enter text: ", font=('fixedsys', 16, "bold"), fg="black")
		text_label.grid(row=0, column=0, padx=20, pady=20)

		scroll_text = ttk.Scrollbar(main, orient=VERTICAL)
		text_box = Text(main, height=8, width=40, pady=10, yscrollcommand=scroll_text.set, bg='white')
		text_box.grid(row=1, column=0, pady=1, padx=1)
		scroll_text.config(command=text_box.yview)
		scroll_text.grid(row=1, column=1, sticky='NS')


		scroll_text2 = ttk.Scrollbar(main, orient=VERTICAL)
		new_text = Text(main, height=8, width=40, pady=10, yscrollcommand=scroll_text2.set, bg='white')
		new_text.grid(row=1, column=2, columnspan=2, padx=(10, 0))
		scroll_text2.config(command=new_text.yview)
		scroll_text2.grid(row=1, column=4, sticky='NS')
		return text_box, new_text

	################################################################################################################################
	def RSA_cipher():  # 1st cipher
		remove()

		key_label = Label(main, text="Enter e: ", font=('fixedsys', 14), pady=15, fg="black")
		key_label.grid(row=2, column=0)
		key_label = Label(main, text="Enter p: ", font=('fixedsys', 14), pady=15, fg="black")
		key_label.grid(row=2, column=1)
		key_label = Label(main, text="Enter q: ", font=('fixedsys', 14), pady=15, fg="black")
		key_label.grid(row=2, column=2)
		key_e = Entry(main, width=20)
		key_e.grid(row=3, column=0, padx=10, pady=10)
		key_p = Entry(main, width=20)
		key_p.grid(row=3, column=1, padx=10, pady=10)
		key_q = Entry(main, width=20)
		key_q.grid(row=3, column=2, padx=10, pady=10)

		text_box, new_text = lab()
		sample = ""
		new_text.insert(1.0, sample)
		label = Label(main, text="RSA Encryption" , font=('Times New Roman', 16, "bold"),bg="white")
		label.grid(row=0, column=1)
		
		#Add insert file/image selection
		file_type = ttk.Combobox(main)
		file_type['values'] = ("text", "image", "file")
		file_type.current(0)
		file_type.grid(row=5, column=0)

		def encrypt():
			cipher_type = file_type.get()
			new_text.delete('1.0', END)
			txt = text_box.get("1.0", END)
			e = int(key_e.get())
			p = int(key_p.get())
			q = int(key_q.get())
			if cipher_type == "text":
				enc_text, cipherTextArray = rsaC.encryption(txt, e, p, q)
				new_text.insert(1.0, enc_text)
			elif cipher_type == "image":
				txt = txt.strip()
				rsaC.encryptionImage(txt, e, p, q)
				new_text.insert(1.0, "New Image File in ./encryptedImage.jpg")
			else:
				txt = txt.strip()
				rsaC.encryptionFile(txt, e, p, q)
				new_text.insert(1.0, "New File in ./encryptedFile.c")
			
		enc = Button(main, text="Encrypt", bd=10, width=10, command=encrypt,bg='#3FBE7F', fg='white')
		enc.grid(row=0, column=2, padx=20, pady=30)
		def decrypt():
			cipher_type = file_type.get()
			new_text.delete('1.0', END)
			txt = text_box.get("1.0", END)
			e = int(key_e.get())
			p = int(key_p.get())
			q = int(key_q.get())
			if cipher_type == "text":	
				enc_text, cipherTextArray = rsaC.encryption(txt, e, p, q)
				dec_text = rsaC.decryption(cipherTextArray, e, p, q)
				new_text.insert(1.0, dec_text)
			elif cipher_type == "image":
				txt = txt.strip()
				new_text.insert(1.0, "New Image File in ./decryptedImage.jpg")
			else:
				txt = txt.strip()
				rsaC.decryptionFile(e, p, q)
				new_text.insert(1.0, "New File in ./decryptedFile.c")

		dec = Button(main, text="Decrypt", bd=10, width=10, command=decrypt,bg='tomato2', fg='white')
		dec.grid(row=0, column=3, padx=10, pady=10)

	#############################################################################################################################


	##############################################################################################################################
	def vignere_cipher():
		remove()

		key_label = Label(main, text="Enter key: ", font=('Kokila', 14), pady=15,
						  bg='black', fg="white")
		key_label.grid(row=2, column=0)
		key_text = Entry(main, width=40)
		key_text.grid(row=3, column=0, padx=10, pady=10)

		text_box, new_text = lab()
		label = Label(main, text="vignere_cipher")
		label.grid(row=0, column=1)

		def encrypt():
			txt = text_box.get("1.0", END)
			key = key_text.get()
			enc_text = vignereC.encrypt(txt, key)
			text_box.delete('1.0', END)
			text_box.insert(1.0, enc_text)

		enc = Button(main, text="Encrypt", bd=10, width=10, command=encrypt,
					 bg='#3FBE7F', fg='white')
		enc.grid(row=0, column=2, padx=20, pady=30)

		def decrypt():
			txt = text_box.get("1.0", END)
			key = key_text.get()
			dec_text = vignereC.decrypt(txt, key)
			text_box.delete('1.0', END)
			text_box.insert(1.0, dec_text)

		dec = Button(main, text="Decrypt", bd=10, width=10, command=decrypt,
					 bg='tomato2', fg='white')
		dec.grid(row=0, column=3, padx=10, pady=10)

	#############################################################################################################################

	################################################################################################################################

	def DES3_cipher():
		remove()

		list_key = ttk.Combobox(main)
		list_key['values'] = (2, 3, 4, 5, 6, 7, 8)
		list_key.current(0)
		list_key.grid(row=5, column=0)

		text_box, new_text = lab()
		sample = " "
		new_text.insert(1.0, sample)
		label = Label(main, text="Triple DES")
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
	def AES_cipher():
		remove()

		label_key = Label(main, text="Enter 16-character key: ", font=('fixedsys', 14), pady=15, fg="black")
		label_key.grid(row=2, column=0)
		entry_key = Entry(main, width=20)
		entry_key.grid(row=3, column=0, padx=10, pady=10)

		text_box, new_text = lab()
		sample = ""
		new_text.insert(1.0, sample)
		label = Label(main, text="AES Encryption" , font=('Times New Roman', 16, "bold"), bg="white")
		label.grid(row=0, column=1)
		
		file_type = ttk.Combobox(main)
		file_type['values'] = ("text", "image", "file")
		file_type.current(0)
		file_type.grid(row=5, column=0)

		def encrypt():
			cipher_type = file_type.get()
			new_text.delete('1.0', END)
			txt = text_box.get("1.0", END).strip()
			key = entry_key.get().strip()
			key = list(bytes(key, encoding='utf-8'))
			if cipher_type == "text":
				enc_text = aesC.encrypt_text(txt, key)
				new_text.insert(1.0, enc_text)
			elif cipher_type == "image":
				filename = txt
				outfilename = aesC.encrypt_image(filename, key)
				new_text.insert(1.0, outfilename)
			else:
				filename = txt
				outfilename = aesC.encrypt_file(filename, key)
				new_text.insert(1.0, outfilename)
			
		enc = Button(main, text="Encrypt", bd=10, width=10, command=encrypt,bg='#3FBE7F', fg='white')
		enc.grid(row=0, column=2, padx=20, pady=30)
		def decrypt():
			cipher_type = file_type.get()
			text_box.delete('1.0', END)
			txt = new_text.get("1.0", END).strip()
			key = entry_key.get().strip()
			key = list(bytes(key, encoding='utf-8'))
			if cipher_type == "text":	
				dec_text = aesC.decrypt_text(txt, key)
				text_box.insert(1.0, dec_text)
			elif cipher_type == "image":
				filename = txt
				outfilename = aesC.decrypt_image(filename, key)
				text_box.insert(1.0, outfilename)
			else:
				filename = txt
				outfilename = aesC.decrypt_file(filename, key)
				text_box.insert(1.0, outfilename)

		dec = Button(main, text="Decrypt", bd=10, width=10, command=decrypt,bg='tomato2', fg='white')
		dec.grid(row=0, column=3, padx=10, pady=10)

	btn_rsa = Button(left_frame, padx=20, bd=10, text='RSA Cipher', width=20, height=3, command=RSA_cipher,
                     bg='white', fg='red', activebackground='black', font=('arial', 16, 'bold'),
					 activeforeground='#3FBE4F')
	btn_rsa.grid(row=1, column=0)

	btn_vig = Button(left_frame, padx=20, bd=10, text='Vignere Cipher', width=20, height=3, command=vignere_cipher,
					 bg='white', fg='red', activebackground='black', font=('arial', 16, 'bold'),
					 activeforeground='#3FBE4F')
	btn_vig.grid(row=2, column=0)

	btn_des3 = Button(left_frame, padx=20, bd=10, text='Triple DES Cipher', width=20, height=3,
					  command=DES3_cipher, bg='white', fg='red', activebackground='black',
					  font=('arial', 16, 'bold'), activeforeground='#3FBE4F')
	btn_des3.grid(row=3, column=0)

	btn_aes = Button(left_frame, padx=20, bd=10, text='AES Cipher', width=26, height=3,
				     command=AES_cipher, bg='white', fg='red', font=('arial', 12, 'bold'),
					 activebackground='black', activeforeground='SeaGreen1')
	btn_aes.grid(row=4, column=0)

	btn_exit = Button(left_frame, text="Exit", padx=20, bd=10, width=23,height=3, command=window.destroy, activebackground="white",
				  bg='black', fg="white", font=('arial', 12, 'bold'), activeforeground="black")
	btn_exit.grid(row=15, column=0)

	window.mainloop()


label_welcome = Label(root, text="Computer Security Final Project\n Topic 1 by: Lindsey Michie, Gabriel Simoes & Marcelo Piccolotto", padx=10, pady=30, bg="light gray", fg="black",
					  font=("Helvetica", 20, "bold")).pack(pady=30)
btn_cipher = Button(root, text="Algorithms", padx=20, bd=10, width=20, height=3, command=cipher, bg="light gray",
					fg="black", activebackground='black', activeforeground='white')
btn_cipher.pack(pady=30)


root.mainloop()