def encrypt_vigenere(plaintext, keyword):
    ciphertext = ""
    if len(keyword) < len(plaintext):
        div = len(plaintext) // len(keyword)
        mod = len(plaintext) % len(keyword)
        s = keyword
        for i in range(div-1):
            keyword += s
        for i in range(mod):
            keyword += keyword[i]
    for i in range(len(keyword)):
        if 'A' <= keyword[i] <= 'Z':
            value = ord(keyword[i]) - 65
        else:
            value = ord(keyword[i]) - 97
        index = ord(plaintext[i]) + value
        if chr(index) > 'z' or 'Z' < chr(index) < 'a' or ('A' < plaintext[i] < 'Z' and "a" <= chr(index)):
            index -= 26
        ciphertext += chr(index)
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    plaintext = ""
    if len(keyword) < len(ciphertext):
        div = len(ciphertext) // len(keyword)
        mod = len(ciphertext) % len(keyword)
        s = keyword
        for i in range(div-1):
            keyword += s
        for i in range(mod):
            keyword += keyword[i]
    for i in range(len(keyword)):
        if 'A' <= keyword[i] <= 'Z':
            value = ord(keyword[i]) - 65
        else:
            value = ord(keyword[i]) - 97
        index = ord(ciphertext[i]) - value
        if chr(index) < 'A' or 'Z' < chr(index) < 'a' or ('a' < ciphertext[i] < 'z' and chr(index) <= 'Z'):
            index += 26
        plaintext += chr(index)
    return plaintext
