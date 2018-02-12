'''
    Author : Saradhi Ramakrishna
    Roll No : 2017H1030081H
    M.E Computer Science , BITS PILANI HYDERABAD CAMPUS
    Description : Takes Cipher text as input and gives the Plain text as output
                Input - 1.Key
                        2.Cipher Text
                Output - Decrypted Plain Text
    Steps : 1. Shifts the cipher in the length of key by 0,1,2,3,.... (SUBTRACTION)
            2. Applies Vignere Cipher Decryption Procedure by repeating the key until it satisfies
               the cipher text length.
            3. Finally prints the decrypted plain text onto the console.
'''

file1 = open("h20171030081_decrypted.txt","r")
originalcipher = file1.read().strip()
key = "edgarcodd"
cipheraftershifting = ""
currentlength = 0;
currentshift = -1;


'''
    Function which returns the decrypted character in vignere cipher by taking
    a single encrypted character and single key character.
'''
def getDecryptedCharInVignere(enc,key):
    e = ord(enc)
    k = ord(key)
    d = ((e - k + 26) % 26) + 65   # d = ((e - k + 26) mod 26) + 65
    return chr(d)


''' 
    Shifting Original Cipher by 0,1,2,3.... in the length of key repetitively
'''
for c in originalcipher:
    if ord(c) >=65 and ord(c) <=90:
        if ((currentlength % len(key)) == 0):
            currentlength = 0;
            currentshift += 1;
        res = ord(c) - (currentshift % 26)
        if res < 65:
            res += 26
        cipheraftershifting += str(chr(res))
        currentlength = currentlength + 1
    elif ord(c) >=97 and ord(c) <= 122:
        if ((currentlength % len(key)) == 0):
            currentlength = 0;
            currentshift += 1;
        res = ord(c.upper()) - (currentshift % 26)   # Shifting by 0,1,2,3,... (Subtraction)
        if res < 65:
            res += 26
        cipheraftershifting += str(chr(res).lower())
        currentlength = currentlength + 1
    else:
        cipheraftershifting += str(c)


currentlength = 0;
plaintextafterdecryption = ""

''' 
    Applying Vignere Cipher breaking procedure and getting the plain text.
    Key is repeated in lengths of its size until it satisfies the plain text length.
'''
for c in cipheraftershifting:
    if ord(c) >= 65 and ord(c) <= 90:
        if ((currentlength % len(key)) == 0):
            currentlength = 0;
        plaintextafterdecryption += getDecryptedCharInVignere(c.upper(),key[currentlength].upper())
        currentlength = currentlength + 1
    elif ord(c) >= 97 and ord(c) <= 122:
        if ((currentlength % len(key)) == 0):
            currentlength = 0;
        plaintextafterdecryption += getDecryptedCharInVignere(c.upper(),key[currentlength].upper()).lower()
        currentlength = currentlength + 1
    else:
        plaintextafterdecryption += str(c)

print plaintextafterdecryption








