'''
    Author : Saradhi Ramakrishna
    Roll No : 2017H1030081H
    M.E Computer Science , BITS PILANI HYDERABAD CAMPUS
    Description : Takes Plain text as input and gives the Cipher text as output
                Input - 1.Key
                        2.Cipher Text
                Output - Plain Text
    Steps : 1. Applies Vignere Cipher Encryption Procedure by repeating the key until it satisfies
               the Plain text length.
            2. Shifts the cipher in the length of key by 0,1,2,3,.... (ADDITION)
            3. Finally prints the Cipher text onto the console.
'''


'''
    Function which returns the encrypted character in vignere cipher by taking
    a single plain character and single key character.
'''
def getEncryptedCharInVignere(plain,key):
    p = ord(plain)
    k = ord(key)
    e = ((p + k) % 26) + 65   # e = ((p + k)mod 26) + 65
    return chr(e)

file1 = open("PlainText.txt","r")
plaintext = file1.read().strip()
key = "edgarcodd"
currentlength = 0;
cipheraftervignere = ""

''' 
    Applying Vignere Encryption Cipher procedure and getting the Cipher text.
    Key is repeated in lengths of its size until it satisfies the plain text length.
'''
for c in plaintext:
    if ord(c) >= 65 and ord(c) <= 90:
        if ((currentlength % len(key)) == 0):
            currentlength = 0;
        cipheraftervignere += getEncryptedCharInVignere(c.upper(),key[currentlength].upper())
        currentlength = currentlength + 1
    elif ord(c) >= 97 and ord(c) <= 122:
        if ((currentlength % len(key)) == 0):
            currentlength = 0;
        cipheraftervignere += getEncryptedCharInVignere(c.upper(),key[currentlength].upper()).lower()
        currentlength = currentlength + 1
    else:
        cipheraftervignere += str(c)
#print cipheraftervignere

currentlength = 0;
currentshift = -1;
finalcipheraftershift = ""

''' 
    Shifting Vignere Cipher by 0,1,2,3.... in the length of key repetitively (Addition)
'''
for c in cipheraftervignere:
    if ord(c) >=65 and ord(c) <=90:
        if ((currentlength % len(key)) == 0):
            currentlength = 0;
            currentshift += 1;
        res = ord(c) + (currentshift % 26)          # Shifting by 0,1,2,3,... (Addition)
        if res > 90:
            res -= 26
        finalcipheraftershift += str(chr(res))
        currentlength = currentlength + 1
    elif ord(c) >=97 and ord(c) <= 122:
        if ((currentlength % len(key)) == 0):
            currentlength = 0;
            currentshift += 1;
        res = ord(c.upper()) + (currentshift % 26)   # Shifting by 0,1,2,3,... (Addition)
        if res > 90:
            res -= 26
        finalcipheraftershift += str(chr(res).lower())
        currentlength = currentlength + 1
    else:
        finalcipheraftershift += str(c)

print finalcipheraftershift

