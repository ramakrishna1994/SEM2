'''
    Author : Saradhi Ramakrishna
    Roll No : 2017H1030081H
    M.E Computer Science , BITS PILANI HYDERABAD CAMPUS
    Description : Takes Cipher text as input and shifts the Cipher text by 0,1,2,3....
                    in lengths of 9.
'''


file1 = open("h20171030081_decrypted_without_spch.txt","r")
originalcipher = file1.read().upper().strip()
key = "EDGARCODD"
currentlength = 0;
currentshift = -1;
cipheraftershifting = ""




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


print cipheraftershifting