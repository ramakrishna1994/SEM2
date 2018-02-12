'''
    Author : Saradhi Ramakrishna
    Roll No : 2017H1030081H
    M.E Computer Science , BITS PILANI HYDERABAD CAMPUS
    Description : Takes Cipher text with special characters as input and gives the Cipher text
                    without characters as output
'''



import re
string = open('h20171030081_decrypted.txt').read()
new_str = re.sub('[^a-zA-Z]', '', string)
open('h20171030081_decrypted_without_spch.txt', 'w').write(new_str.upper())


