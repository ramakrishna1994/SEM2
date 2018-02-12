'''
    Author : Saradhi Ramakrishna
    Roll No : 2017H1030081H
    M.E Computer Science , BITS PILANI HYDERABAD CAMPUS
    Description : Takes Cipher as input and gives the Frequency of bi-grams,tri-grams
                    and poly-grams.
'''

file1 = open("sample.txt","r")
ciphertext = file1.read().strip()

print "Length of Cipher text = " +str(len(ciphertext))
countList = [0] * 10000

for i in range(0,len(ciphertext)-1):
    for j in range(i+1,len(ciphertext)-1):
        oldstring = ciphertext[i:j+1]
        newstring = ciphertext[j+1:len(ciphertext)]
        index = newstring.find(oldstring)
        if(index > 0):
            b = index+len(oldstring)
            countList[b] += 1

max = -1
index = -1
for i in range(0,len(countList)-1):
    if max < countList[i]:
        max = countList[i]
        index = i
print "maximum value is = " + str(max)
print "maximum index is = " + str(index)

print "---------------- Frequency Table---------------"
print "length | value"
for i in range(0,index+1):
    print str(i) + " | " + str(countList[i])


