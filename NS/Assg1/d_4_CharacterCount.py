'''
    Author : Saradhi Ramakrishna
    Roll No : 2017H1030081H
    M.E Computer Science , BITS PILANI HYDERABAD CAMPUS
    Description : Takes Cipher text as input and prints the character count
'''

file1 = open("sample.txt","r")
ciphertext = file1.read().strip()

count = [0]*26

for c in ciphertext:
    if ord(c) >=65 and ord(c) <= 90:
        count[ord(c)-65] += 1

max = -1
for i in range(0,len(count)):
    if max < count[i]:
        max =count[i]
        index = i

print "Maximum Frequent Character count is " + str(max)
print "Character = " + str(chr(index+65))

print "--------------- Character Frequency Table --------------------"

for i in range(0,len(count)):
    print str(chr(i+65)) + " | " + str(count[i])
