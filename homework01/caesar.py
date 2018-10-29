def encrypt_caesar(plaintext):
    ciphertext = ''
    for i in plaintext:
        value = ord(i)
        if (value >= 65 and value <= 90) or (value >= 97 and value <= 122):
            if (i == 'X'):
                ciphertext += 'A'
            elif (i == 'Y'):
                ciphertext += 'B'
            elif (i == 'Z'):
                ciphertext += 'C'
            elif (i == 'x'):
                ciphertext += 'a'
            elif (i == 'y'):
                ciphertext += 'b'
            elif (i == 'z'):
                ciphertext += 'c'
            else:
                ciphertext += chr(value+3)
        else:
            ciphertext += i
    return ciphertext

def decrypt_caesar(ciphertext):
    plaintext = ''
    for i in ciphertext:
        value = ord(i)
        if (value >= 65 and value <= 90) or (value >= 97 and value <= 122):
            if (i == 'A'):
                plaintext += 'X'
            elif (i == 'B'):
                plaintext += 'Y'
            elif (i == 'C'):
                plaintext += 'Z'
            elif (i == 'a'):
                plaintext += 'x'
            elif (i == 'b'):
                plaintext += 'y'
            elif (i == 'c'):
                plaintext += 'z'
            else:
                plaintext += chr(value-3)
        else:
            plaintext += i
    return plaintext

