def encrypt_vigenere(plaintext, keyword):
    ciphertext = ''
    if keyword == 'A' or keyword == 'a':
        ciphertext = plaintext
        return ciphertext
    if len(keyword) < len(plaintext):
        k = len(plaintext)//len(keyword)
        d = len(plaintext)%len(keyword)
        keyword1 = keyword
        for i in range(k-1):
            keyword += keyword1
        i = 0
        while d > 0:
            keyword += keyword[i]
            i += 1
            d -= 1
    for i in range(len(plaintext)):
        vt1 = ord(plaintext[i])
        vt2 = ord(keyword[i])
        if (vt1 < 65) or ((vt1 > 90) and (vt1 < 97)) or (vt1 > 122):
            ciphertext += plaintext[i]
        else:
            value = vt2 - 65
            if (vt1 >= 65) and (vt1 <= 90):
                k = value + vt1 - 90
                if k > 0:
                    value =(value + vt1) - 90
                    ciphertext += chr(64 + value)
                else:
                    ciphertext += chr(value + vt1)
            if (vt1 >= 97) and (vt1 <= 122):
                value = vt2 - 97
                k = value + vt1 - 122
                if k > 0:
                    value = k
                    ciphertext += chr(96 + value)
                else:
                    ciphertext += chr(value + vt1)
    return ciphertext

def decrypt_vigenere(ciphertext, keyword):
    plaintext = ''
    if (keyword == 'A') or (keyword == 'a'):
        plaintext = ciphertext
        return plaintext
    if len(keyword) < len(ciphertext):
        k = len(ciphertext)//len(keyword)
        d = len(ciphertext)%len(keyword)
        keyword1 = keyword
        for i in range(k-1):
            keyword += keyword1
        i = 0
        while d > 0:
            keyword += keyword[i]
            i += 1
            d -= 1
    for i in range(len(ciphertext)):
        vt1 = ord(ciphertext[i])
        vt2 = ord(keyword[i])
        value = vt1 - vt2 + 65
        if (vt1 < 65) or ((vt1 > 90) and (vt1 < 97)) or (vt1 > 122):
            ciphertext += plaintext[i]
            continue
        if (vt1 >= 65) and (vt1 <= 90):
            k = vt1 - vt2
            if k < 0:
                value = 91 + k
                plaintext += chr(value)
            else:
                plaintext += chr(65 + k)
        if (vt1 >= 97) and (vt1 <= 122):
            k = vt1 - vt2
            if k < 0:
                value = 123 + k
                plaintext += chr(value)
            else:
                plaintext += chr(97 + k)
    return plaintext

