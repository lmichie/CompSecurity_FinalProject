import binascii
from bitstring import BitArray

permutation_table_1 = [56, 48, 40, 32, 24, 16,  8,
                       0, 57, 49, 41, 33, 25, 17,
                       9,  1, 58, 50, 42, 34, 26,
                       18, 10,  2, 59, 51, 43, 35,
                       62, 54, 46, 38, 30, 22, 14,
                       6, 61, 53, 45, 37, 29, 21,
                       13,  5, 60, 52, 44, 36, 28,
                       20, 12,  4, 27, 19, 11,  3
                       ]

permutation_table_2 = [
    13, 16, 10, 23,  0,  4,
    2, 27, 14,  5, 20,  9,
    22, 18, 11,  3, 25,  7,
    15,  6, 26, 19, 12,  1,
    40, 51, 30, 36, 46, 54,
    29, 39, 50, 44, 32, 47,
    43, 48, 38, 55, 33, 52,
    45, 41, 49, 35, 28, 31
]

left_rotations = [
    1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
]

initial_permutation_table = [57, 49, 41, 33, 25, 17, 9,  1,
                             59, 51, 43, 35, 27, 19, 11, 3,
                             61, 53, 45, 37, 29, 21, 13, 5,
                             63, 55, 47, 39, 31, 23, 15, 7,
                             56, 48, 40, 32, 24, 16, 8,  0,
                             58, 50, 42, 34, 26, 18, 10, 2,
                             60, 52, 44, 36, 28, 20, 12, 4,
                             62, 54, 46, 38, 30, 22, 14, 6
                             ]

expansion_table = [
    31,  0,  1,  2,  3,  4,
    3,  4,  5,  6,  7,  8,
    7,  8,  9, 10, 11, 12,
    11, 12, 13, 14, 15, 16,
    15, 16, 17, 18, 19, 20,
    19, 20, 21, 22, 23, 24,
    23, 24, 25, 26, 27, 28,
    27, 28, 29, 30, 31,  0
]

p_table = [
    15, 6, 19, 20, 28, 11,
    27, 16, 0, 14, 22, 25,
    4, 17, 30, 9, 1, 7,
    23, 13, 31, 26, 2, 8,
    18, 12, 29, 5, 21, 10,
    3, 24
]

s_tables = [
    # S1
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
     0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
     4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
     15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

    # S2
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
     3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
     0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
     13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

    # S3
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
     13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
     13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
     1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

    # S4
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
     13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
     10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
     3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

    # S5
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
     14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
     4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
     11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

    # S6
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
     10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
     9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
     4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

    # S7
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
     13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
     1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
     6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

    # S8
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
     1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
     7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
     2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
]

final_permutation_table = [
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25,
    32,  0, 40,  8, 48, 16, 56, 24
]


def table_permute(block, table):
    result = []

    for i in range(len(table)):
        result.append(block[table[i]])

    return ''.join(result)


def leftrotate(s, d):
    tmp = s[d:] + s[0: d]
    return tmp


def toBinary(a):
    res = ''.join(format(ord(i), '08b') for i in a)
    return res


def generate_binary_blocks(binary):
    counter = 0
    blocks = []
    block = []
    for bit in binary:
        if counter == 64:
            blocks.append(block.copy())
            block = []
            counter = 0
        block.append(bit)
        counter += 1
    if len(block):
        blocks.append(block)

    while len(blocks[-1]) < 64:
        blocks[-1].append('0')

    for i, block in enumerate(blocks):
        blocks[i] = ''.join(block)

    return blocks


def substitution(block):
    result = []

    curr_table = 0

    six_bit_block = []
    for bit in block:
        six_bit_block.append(bit)
        if (len(six_bit_block) == 6):
            row = int(six_bit_block[0] + six_bit_block[5], 2)
            col = int(six_bit_block[1] + six_bit_block[2] +
                      six_bit_block[3] + six_bit_block[4], 2)
            result.append("{0:04b}".format(s_tables[curr_table][16*row + col]))
            six_bit_block = []
            curr_table += 1

    return ''.join(result)


def f_function(block, key):
    return table_permute(substitution(xor(table_permute(block, expansion_table), key)), p_table)


def xor(a, b):
    result = ''

    for i in range(len(a)):
        if a[i] == b[i]:
            result += '0'
        else:
            result += '1'

    return result


def generate_keys(key):
    permuted_key = table_permute(key, permutation_table_1)
    l = ''.join(permuted_key[:28])
    r = ''.join(permuted_key[28:])

    left_subkeys = []
    right_subkeys = []

    rotations = 0

    for i in range(len(left_rotations)):
        rotations += left_rotations[i]
        left_subkeys.append(leftrotate(l, rotations))
        right_subkeys.append(leftrotate(r, rotations))

    permutation_2_keys = []

    for i in range(len(left_rotations)):
        permutation_2_keys.append(table_permute(
            left_subkeys[i] + right_subkeys[i], permutation_table_2))

    return permutation_2_keys

def remove_padding(padded_binary):
    index = len(padded_binary) - 1

    while(not (padded_binary[index] == '1' and padded_binary[index - 1] == '1' and padded_binary[index - 2] == '1' and padded_binary[index - 3] == '1')):
        index -= 1

    return padded_binary[:index -3]

    


def DES(blocks, keys):
    results = []

    for block in blocks:

        ip = table_permute(block, initial_permutation_table)

        l_0 = ip[:32]
        r_0 = ip[32:]

        for i in range(len(keys)):
            r_1 = xor(f_function(r_0, keys[i]), l_0)

            l_0 = r_0
            r_0 = r_1

        results.append(table_permute(r_0 + l_0, final_permutation_table))

    return''.join(results)



def single_encrypt(message, key):
    keys = generate_keys(key)
    blocks = generate_binary_blocks(message)
    cipher = DES(blocks, keys)
    return cipher


def single_decrypt(cyphertext, key):
    keys = generate_keys(key)
    keys.reverse()
    blocks = generate_binary_blocks(cyphertext)
    plain_binary = DES(blocks, keys)
    return plain_binary


def encrypt(message, key_1, key_2, key_3):
    cipher = single_encrypt(message, key_1)
    cipher = single_decrypt(cipher, key_2)
    cipher = single_encrypt(cipher, key_3)
    return cipher


def decrypt(cipher, key_1, key_2, key_3):
    message = single_decrypt(cipher, key_3)
    message = single_encrypt(message, key_2)
    message = single_decrypt(message, key_1)
    return message


def binary_to_plaintext(binary):
    try:
        return binascii.unhexlify('%x' % int(binary, 2)).decode()
    except:
        return "Error: could not translate to ascii"

def encrypt_text(plain_text, key1, key2, key3):
    return encrypt(toBinary(plain_text) + '1111', key1, key2, key3)

def decrypt_text(cypher_binary, key1, key2, key3):
    return binary_to_plaintext(remove_padding(decrypt(cypher_binary, key1, key2, key3)))

def encrypt_image(filename, key1, key2, key3):
    with open(filename, "rb") as img_file:
        img = bytes(img_file.read())
    plain_binary = BitArray(img)
    cipher = encrypt(plain_binary.bin + '1111', key1, key2, key3)
    with open('./encryptedImage.jpeg', 'wb') as out:
        out.write(bytes(bits_to_bytes(cipher)))
    return "./encryptedImage.jpeg"

def decrypt_image(filename, key1, key2, key3):
    with open(filename, "rb") as cipher_file:
        cipher = bytes(cipher_file.read())
    plain_binary = BitArray(cipher)
    img = remove_padding(decrypt(plain_binary.bin, key1, key2, key3))
    with open('./decryptedImage.jpeg', 'wb') as out:
        out.write(bytes(bits_to_bytes(img)))
    return './decryptedImage.jpeg'

def encrypt_file(filename,  key1, key2, key3):
    with open(filename, "r", newline="\n") as text_file:
        text = bytes(text_file.read(), encoding='utf8')
    plain_binary = BitArray(text)
    cipher = encrypt(plain_binary.bin + '1111', key1, key2, key3)
    with open('./encryptedFile.c', 'wb') as out:
        out.write(bytes(bits_to_bytes(cipher)))
    return "./encryptedFile.c"

def decrypt_file(filename, key1, key2, key3):
    with open(filename, "rb") as cipher_file:
        cipher = bytes(cipher_file.read())
    cypher_binary = BitArray(cipher)
    text = remove_padding(decrypt(cypher_binary.bin, key1, key2, key3))
    text = bytes(bits_to_bytes(text)).decode("utf-8") 
    with open('./decryptedFile.c', 'w', newline="\n") as out:
        out.write(text)
    return "./decryptedFile.c"

def bits_to_bytes(bits):
    it = 8
    result = []
    while it <= len(bits):
        result.append(int(bits[it-8:it],2))
        it += 8
    return result