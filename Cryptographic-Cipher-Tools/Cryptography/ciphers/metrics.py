from collections import defaultdict
from time import time
import matplotlib.pyplot as plt
import numpy as np
import rsaC, vigenereC, aesC, tripleC

lengths = [10, 100, 1000, 10000]
duration = defaultdict(list)

for length in lengths:
    runs = 10
    text = 'a' * length
    
    print('length:', length)
    
    total = 0
    key = 'ndsecure'
    for _i in range(runs):
        start = time()
        assert text == vigenereC.decrypt(vigenereC.encrypt(text, key), key)
        total += time() - start
    duration['vigenere'].append(total/runs)
    
    total = 0
    e = 65537
    d = 52203292265329821477201215331647767385
    n = 109658872566201497189314566136483333067
    key = (e, d, n)
    for _i in range(runs):
        start = time()
        assert text == rsaC.decrypt_text(rsaC.encrypt_text(text, key), key)
        total += time() - start
    duration['rsa'].append(total/runs)
    
    total = 0
    key0 = "0000000011111111000000001111111100000000111111110000000011111111"
    key1 = "0000000000000000000000000000000000000000000000000000000000000000"
    key2 = "1111111111111111111111111111111111111111111111111111111111111111"
    for _i in range(runs):
        start = time()
        r = tripleC.encrypt_text(text, key0, key1, key2)
        r = tripleC.decrypt_text(r, key0, key1, key2)
        assert text == r
        total += time() - start
    duration['3des'].append(total/runs)
    
    total = 0
    key = list(bytes('ndsecurendsecure', encoding='utf-8'))
    for _i in range(runs):
        start = time()
        assert text == aesC.decrypt_text(aesC.encrypt_text(text, key), key)
        total += time() - start
    duration['aes'].append(total/runs)
    
# set width of bar
bar_width = 0.1
fig = plt.subplots(figsize =(12, 8))
 
# set height of bar
IT = [12, 30, 1, 8, 22]
ECE = [28, 6, 16, 5, 10]
CSE = [29, 3, 24, 25, 17]
 
# Set position of bar on X axis
br1 = [bar_width + x - 1.5 * bar_width for x in np.arange(len(lengths))]
br2 = [bar_width + x - 0.5 * bar_width for x in np.arange(len(lengths))]
br3 = [bar_width + x + 0.5 * bar_width for x in np.arange(len(lengths))]
br4 = [bar_width + x + 1.5 * bar_width for x in np.arange(len(lengths))]
 
# Make the plot
logarithmic_scale = False
plt.bar(br1, duration['vigenere'], width = bar_width, edgecolor ='grey', label ='Vig??n??re', log=logarithmic_scale)
plt.bar(br2, duration['rsa'], width = bar_width, edgecolor ='grey', label ='RSA', log=logarithmic_scale)
plt.bar(br3, duration['3des'], width = bar_width, edgecolor ='grey', label ='3DES', log=logarithmic_scale)
plt.bar(br4, duration['aes'], width = bar_width, edgecolor ='grey', label ='AES', log=logarithmic_scale)
 
# Adding Xticks
plt.xlabel('Message Length', fontweight ='bold', fontsize = 15)
plt.ylabel('Encryption + Decryption Time (s)', fontweight ='bold', fontsize = 15)
plt.xticks([r + bar_width for r in range(len(lengths))], lengths)

plt.title("Algorithm runtime in logarithmic scale")

plt.legend()
plt.show()