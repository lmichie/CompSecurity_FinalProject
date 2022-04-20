# fmt: off

# based on explanation from https://engineering.purdue.edu/kak/compsec/NewLectures/Lecture8.pdf
# and https://crypto.stackexchange.com/questions/2418/how-to-use-rcon-in-key-expansion-of-128-bit-advanced-encryption-standard
RC = [0, 1]
for _i in range(14):
    RC.append((RC[-1] << 1) ^ (0x11b & -(RC[-1] >> 7)))

# values taken from https://engineering.purdue.edu/kak/compsec/NewLectures/Lecture8.pdf
SBOX = [
    99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118,
    202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192,
    183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21,
    4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117,
    9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132,
    83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207,
    208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168,
    81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210,
    205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115,
    96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219,
    224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121,
    231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8,
    186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138,
    112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158,
    225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223,
    140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22,
]

SBOX_INV = [
    82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251,
    124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203,
    84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78,
    8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37,
    114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146,
    108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132,
    144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6,
    208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107,
    58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115,
    150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110,
    71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27,
    252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244,
    31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95,
    96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239,
    160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97,
    23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125,
]

# fmt: on

# implementation based on pseudocode from https://en.wikipedia.org/wiki/Rijndael_MixColumns
def gmul(a, b):
    p = 0
    for _c in range(8):
        if b & 1:
            p ^= a
        # a = (a << 1) ^ (0x11b & -(a >> 7))
        a <<= 1
        if a & 0x100:
            a ^= 0x11b
        b >>= 1
    return p

GMUL = {}
for a in [2, 3, 9, 11, 13, 14]:
    GMUL[a] = tuple(gmul(a, b) for b in range(0x100))


def xor(x, y):
    return [p ^ q for p, q in zip(x, y)]


def rotate_left(x):
    return x[1:] + x[:1]


def sub_bytes(x):
    return [SBOX[p] for p in x]


def inv_sub_bytes(x):
    return [SBOX_INV[p] for p in x]


def add_round_key(state, key):
    return xor(state, key)


def expand_key(key, nrounds):
    exp_key = key.copy()
    for i in range(4, 4 * (nrounds + 1)):
        t = exp_key[(i - 1) * 4 : i * 4]
        if i % 4 == 0:
            t = xor(sub_bytes(rotate_left(t)), [RC[i // 4], 0, 0, 0])
        exp_key.extend(xor(t, exp_key[i * 4 - 16: i * 4 - 12]))
    return exp_key


def sub_bytes(state):
    return [SBOX[b] for b in state]


def inv_sub_bytes(state):
    return [SBOX_INV[b] for b in state]


def shift_rows(state):
    rows = []
    for r in range(4):
        row = state[r::4]  # get row skiping columns of size 4
        row = row[r:] + row[:r]  # move diagonal to first column
        rows.append(row)
    columns = [p for q in zip(*rows) for p in q]
    return columns


def inv_shift_rows(state):
    rows = []
    for r in range(4):
        row = state[r::4]  # get row skiping columns of size 4
        row = row[4 - r :] + row[: 4 - r]  # move first column back to diagonal
        rows.append(row)
    columns = [p for q in zip(*rows) for p in q]
    return columns


# implementation based on https://en.wikipedia.org/wiki/Rijndael_MixColumns
def mix_columns(state):
    result = []
    for c in range(4):
        col = state[c * 4 : (c + 1) * 4]
        r0 = GMUL[2][col[0]] ^ GMUL[3][col[1]] ^ col[2] ^ col[3]
        r1 = col[0] ^ GMUL[2][col[1]] ^ GMUL[3][col[2]] ^ col[3]
        r2 = col[0] ^ col[1] ^ GMUL[2][col[2]] ^ GMUL[3][col[3]]
        r3 = GMUL[3][col[0]] ^ col[1] ^ col[2] ^ GMUL[2][col[3]]
        result.extend([r0, r1, r2, r3])
    return result


def inv_mix_columns(state):
    result = []
    for c in range(4):
        col = state[c * 4 : (c + 1) * 4]
        r0 = GMUL[14][col[0]] ^ GMUL[11][col[1]] ^ GMUL[13][col[2]] ^ GMUL[9][col[3]]
        r1 = GMUL[9][col[0]] ^ GMUL[14][col[1]] ^ GMUL[11][col[2]] ^ GMUL[13][col[3]]
        r2 = GMUL[13][col[0]] ^ GMUL[9][col[1]] ^ GMUL[14][col[2]] ^ GMUL[11][col[3]]
        r3 = GMUL[11][col[0]] ^ GMUL[13][col[1]] ^ GMUL[9][col[2]] ^ GMUL[14][col[3]]
        result.extend([r0, r1, r2, r3])
    return result


def encrypt(message, key, nrounds=10):
    if isinstance(message, bytes) or isinstance(message, bytearray):
        state = list(message)
    elif isinstance(message, str):
        state = list(map(ord, message))
    else:
        state = list(message)
        
    exp_key = expand_key(key, nrounds)
    
    state = add_round_key(state, exp_key[0:16])
    for r in range(1, nrounds):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, exp_key[r * 16 : (r + 1) * 16])
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, exp_key[nrounds * 16 :])
    
    return list(state)

def decrypt(cipher, key, nrounds=10):
    if isinstance(cipher, bytes) or isinstance(cipher, bytearray):
        state = list(cipher)
    elif isinstance(cipher, str):
        state = list(map(ord, cipher))
    else:
        state = list(cipher)
        
    exp_key = expand_key(key, nrounds)
    
    state = add_round_key(state, exp_key[nrounds*16:(nrounds+1)*16])
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    for r in range(nrounds-1, 0, -1):
        state = add_round_key(state, exp_key[r * 16 : (r + 1) * 16])
        state = inv_mix_columns(state)
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
    state = add_round_key(state, exp_key[0:16])
    
    return list(state)


def encrypt_text(text, key, blocksize=16):
    text = text.strip()
    text = bytes(text, encoding='utf-8')
    if blocksize:
        pad_length = 16 - (len(text) % 16)
        text += bytes([pad_length]) * pad_length
    cipher = encrypt(text, key)
    return bytes(cipher).hex()

def decrypt_text(cipher, key, blocksize=16):
    cipher = bytes.fromhex(cipher)
    text = decrypt(cipher, key)
    if blocksize:
        text = text[:-text[-1]]
    text = bytes(text).decode("utf-8") 
    return text

def encrypt_image(filename, key, blocksize=16):
    with open(filename, "rb") as img_file:
        img = bytes(img_file.read())
    if blocksize:
        pad_length = 16 - (len(img) % 16)
        img += bytes([pad_length]) * pad_length
    cipher = encrypt(img, key)
    with open('./encryptedImage.jpeg', 'wb') as out:
        out.write(cipher)
    return "./encryptedImage.jpeg"
	
def decrypt_image(filename, key, blocksize=16):
    with open(filename, "rb") as cipher_file:
        cipher = bytes(cipher_file.read())
    img = decrypt(cipher, key)
    if blocksize:
        img = img[:-img[-1]]
    with open('./decryptedImage.jpeg', 'wb') as out:
        out.write(img)
    return './decryptedImage.jpeg'

def encrypt_file(filename, key, blocksize=16):
    with open(filename, "r") as text_file:
        text = bytes(text_file.read(), encoding='utf8')
    if blocksize:
        pad_length = 16 - (len(text) % 16)
        text += bytes([pad_length]) * pad_length
    cipher = encrypt(text, key)
    cipher = ''.join(chr(p) for p in cipher)
    with open('./encryptedFile.c', 'w') as out:
        out.write(cipher)
    return "./encryptedFile.c"

def decrypt_file(filename, key, blocksize=16):
    with open(filename, "r") as cipher_file:
        cipher = bytes(cipher_file.read(), encoding='utf8')
    text = decrypt(cipher, key)
    if blocksize:
        text = text[:-text[-1]]
    text = text.decode("utf-8") 
    with open('./decryptedFile.c', 'w') as out:
        out.write(text)
    return "./decryptedFile.c"