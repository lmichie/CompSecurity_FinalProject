import binascii
from math import gcd
p = 448500690975152607978063537675655100228561968640743033264994624907311301727954618776592131432970453319274164757456900360809613450208308427051224715601825715694126659023243326653708932560006426538354434994211909696350939307259469268464399327307567418024237505252087309516604048747469861472120690296679
q = 797142830676371202783106590305499953807978464831617412146739794698696574269657813361892048534053769911087232366556200569808067035904716519320282044787921526677805285799163501701004063525600697748650815091626560388355572839685532622148490117538712600176513505164969571526664640345723199170240816113027

def gen_values():
	n = p * q
	phi = (p-1) * (q-1)

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

def encrypt(plainTexti, e, n):
	plainText = plainText.strip()
	b = bytes(plainText, 'utf-8')
	cipherText = (int.from_bytes(b, byteorder='big', signed=False)**e) % n
	return str(cipherText)

def decrypt(cipherText):
	cipherText = cipherText.strip()
	plainText = pow(int(cipherText), int(d), int(n))
	b = bin(plainText)
	bi = int(b, 2)
	bn = bi.bit_length() * 7 // 8
	ba = bi.to_bytes(bn, "big")
	return str(ba.decode())
