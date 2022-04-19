import binascii
import matplotlib.pyplot as plt
import matplotlib.image as io
from PIL import Image
from math import gcd

def euclid(a, b):
	if b==0:
		return a
	else:
		return euclid(b, a % b)

def extended_euclid(e,phi):
	d=0
	x1=0
	x2=1
	y1=1
	orig_phi = phi
	tempPhi = phi

	while (e>0):
		temp1 = int(tempPhi/e)
		temp2 = tempPhi - temp1 * e
		tempPhi = e
		e = temp2

		x = x2- temp1* x1
		y = d - temp1 * y1

		x2 = x1
		x1 = x
		d = y1
		y1 = y

		if tempPhi == 1:
			d += phi
			break
	return d

####	BASIC TEXT	####
def encryption(plainText, e, p, q):
	n = p * q
	plainText = plainText.strip()
	letters = list(plainText)
	cipherText = []
	num = ""
	for i in range(0,len(letters)):
		c = (ord(letters[i])**e)%n
		cipherText += [c]
		num += chr(c)
	return str(num), cipherText

def decryption(cipherTextArray, e, p, q):
	phi = (p-1) * (q-1)
	n = p * q
	#calculate d
	d = extended_euclid(e,phi)
	plainText = []
	num = ""
	for i in range(0,len(cipherTextArray)):
		c = (cipherTextArray[i]**d)%n
		plainText += [c]
		num += chr(c)
	return str(num)

####	IMAGE FILE	####
def encryptionImage(plainText, e, p, q):
	n = p * q
	my_img = io.imread(plainText)
	height, width = my_img.shape[0], my_img.shape[1]
	encrypt = [[0 for x in range(10000)] for y in range(10000)]
	for i in range(0, height):
		for j in range(0, width):
			r, g, b = my_img[i, j]
			print(my_img[i,j])
			C1 = (r**e)%n
			C2 = (g**e)%n
			C3 = (b**e)%n
			encrypt[i][j] = [C1, C2, C3]
			C1 = C1 % 256
			C2 = C2 % 256
			C3 = C3 % 256
			my_img[i, j] = [C1, C2, C3]
	io.imsave("./encryptedImage.jpeg",my_img)
	
	phi = (p-1) * (q-1)
	d = extended_euclid(e,phi)
	for i in range(0, height):
		for j in range(0, width):
			r, g, b = encrypt[i][j]
			M1 = pow(int(r),d,n)
			M2 = (int(g)**d)%n
			M3 = (int(b)**d)%n
			my_img[i, j] = [M1, M2, M3]
	io.imsave("./decryptedImage.jpeg",my_img)
	
def decryptionImage(e, p, q, encrypt, height, width):
		phi = (p-1) * (q-1)
		d = extended_euclid(e,phi)
		for i in range(0, height):
			for j in range(0, width):
				print(encrypt[i][j])
				r, g, b = 1, 2, 3
				M1 = (r**d)%n
				M2 = (g**d)%n
				M3 = (b**d)%n
				my_img[i, j] = [M1, M2, M3]
		fin = open("./decryptedImage.jpeg", 'wb')
		fin.write(my_img)
		fin.close()

####	 FILE	####
def encryptionFile(plainText, e, p, q):
	n = p * q
	fin = open(plainText, 'rb')
	f = fin.read()
	fin.close()
	f = bytearray(f)
	for index, values in enumerate(f):
		f[index] = (values**e)%n

	fin = open("./encryptedFile.c", 'wb')
	fin.write(f)
	fin.close()


def decryptionFile(e, p, q):
	phi = (p-1) * (q-1)
	n = p * q
	#calculate d
	d = extended_euclid(e,phi)
	fin = open("./encryptedFile.c", 'rb')
	f = fin.read()
	fin.close()
	f = bytearray(f)
	for index, values in enumerate(f):
		f[index] = (values**d)%n

	fin = open("./decryptedFile.c", 'wb')
	fin.write(f)
	fin.close()

