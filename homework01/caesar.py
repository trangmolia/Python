def encrypt_caesar(plaintext):
    ciphertext = ""
    for i in plaintext:
        if 'A' <= i <= 'Z' or 'a' <= i <= 'z':
            value = ord(i)+3
            if chr(value) > 'z' or 'Z' < chr(value) < 'a':
                ciphertext += chr(ord(i) - 23)
            else:
                ciphertext += chr(value)
        else:
                ciphertext += i
    return ciphertext


def decrypt_caesar(ciphertext):
    plaintext = ""
    for i in ciphertext:
        if 'A' <= i <= 'Z' or 'a' <= i <= 'z':
            value = ord(i)-3
            if chr(value) < 'A' or 'Z' < chr(value) < 'a':
                plaintext += chr(ord(i) + 23)
            else:
                plaintext += chr(value)
        else:
            plaintext += i
    return plaintext