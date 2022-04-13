import binascii
from math import gcd


def gen_values():
	e = random.randrange(1,phi)
	g = euclid(e,phi)
	while(g!=1):
		e = random.randrange(1,phi)
		g = euclid(e,phi)

	d = extended_euclid(e,phi)
	public_key=(e,n)
	private_key=(d,n)
	return e, d, n

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

def encryptionImage(plainText, e, p, q):
	n = p * q
	fin = open(plainText, 'rb')
	image = fin.read()
	fin.close()
    image = bytearray(image)
	for index, values in enumerate(image):
	#do computation
		image[index] = (values**e)%n

	fin = open(path, 'wb')
	fin.write(image)
	fin.close()

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