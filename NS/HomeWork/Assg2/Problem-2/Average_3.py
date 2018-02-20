'''

@Author : Saradhi Ramakrishna
@ID     : 2017H1030081H
@Description : Below code is practical implementation of Confusion which is finding out the average number of bits change in cipher text when 
				one bit in key is changed.
@Inputs : message and key are read from a file.
@Outputs : Writes average to console.

'''

from BitVector import *
from Tables import *

'''
	S-Boxes used in f method
'''
def sBox(MessageBitVector_48_Bits):
    iteration = 0
    message_32_Bits = ""
    for i in range(0,len(MessageBitVector_48_Bits),6):
        rowBinary = str(MessageBitVector_48_Bits[i])+str(MessageBitVector_48_Bits[i+5])
        rowDecimal = int(rowBinary,2)
        colBinary = str(MessageBitVector_48_Bits[i+1:i+5])
        colDecimal = int(colBinary,2)
        message_32_Bits += str("{0:04b}".format(S_BOX[iteration][rowDecimal][colDecimal]))
        iteration += 1
    return BitVector(bitstring = message_32_Bits).permute(S_BOX_PERMUTE_TABLE_ORIGINAL_MODIFIED)


'''
	Padding function used in encryption procedure if bit vector is having bits less than 64
'''
def returnPadding():
    binString = ""
    for i in range(0,48):
        binString += "0"
    padding = str("0000110100001010") + binString;
    return padding


'''
	function f used for encrypting and decrypting
'''
def f(rightMessageBitVector_32_Bits,keyBitVector_48_Bits):
    rightMessageBitVector_48_Bits = rightMessageBitVector_32_Bits.permute(E_BOX_PERMUTATION_ORIGINAL)
    newrightMessageBitVector_48_Bits = rightMessageBitVector_48_Bits ^ keyBitVector_48_Bits
    result = sBox(newrightMessageBitVector_48_Bits)
    return result

'''
	Calculating number of bits changed in new cipher text compared to old cipher text
'''
def calculateChanges(oldBitString,newBitString):
    bitsChanged = 0
    for i in range(0,len(oldBitString)):
        if oldBitString[i] != newBitString[i]:
            bitsChanged += 1
    return bitsChanged


'''
	A single DES Algorithm procedure for encrypting
'''
def Encryption():
    bitString = ""
    while fullMessageBitVectors.more_to_read:
        keyBitVector_56_Bit = keyBitVector_64_Bits.permute(PC_1_ORIGINAL_MODIFIED)
        [leftKeyBitVector_28_Bits, rightKeyBitVector_28_Bits] = keyBitVector_56_Bit.divide_into_two()
        singleMessageBitVector_64_Bits = fullMessageBitVectors.read_bits_from_file(64)
        if singleMessageBitVector_64_Bits.length() != 64:
            padding = returnPadding()
            Message = str(singleMessageBitVector_64_Bits)+str(padding[0:64-singleMessageBitVector_64_Bits.length()])
            singleMessageBitVector_64_Bits = BitVector(bitstring=Message)
        permutedSingleMessageBitVector_64_Bits = singleMessageBitVector_64_Bits.permute(INITIAL_PERMUTATION_64_BITS_MODIFIED)
        [oldLeftMessageBitVector_32_Bits,oldRightMessageBitVector_32_Bits] = permutedSingleMessageBitVector_64_Bits.divide_into_two()
        for currentIteration in range(0, 16):
            leftKeyBitVector_28_Bits << ITERATION_AND_SHIFTS[currentIteration]
            rightKeyBitVector_28_Bits << ITERATION_AND_SHIFTS[currentIteration]
            newKeyBitVector_56_Bits = leftKeyBitVector_28_Bits + rightKeyBitVector_28_Bits
            keyBitVector_48_Bits = newKeyBitVector_56_Bits.permute(PC_2_ORIGINAL_MODIFIED)
            newLeftMessageBitVector_32_Bits = oldRightMessageBitVector_32_Bits
            newRightMessageBitVector_32_Bits = oldLeftMessageBitVector_32_Bits ^ f(oldRightMessageBitVector_32_Bits,keyBitVector_48_Bits)
            oldLeftMessageBitVector_32_Bits = newLeftMessageBitVector_32_Bits
            oldRightMessageBitVector_32_Bits = newRightMessageBitVector_32_Bits

        reversedMessageBitVector_64_Bits = newRightMessageBitVector_32_Bits + newLeftMessageBitVector_32_Bits  #Reversing
        finalMessageBitVector_64_Bits = reversedMessageBitVector_64_Bits.permute(INVERSE_INITIAL_PERMUTATION_64_BITS_MODIFIED)
        bitString += str(finalMessageBitVector_64_Bits)

    return bitString




fullMessageBitVectors = BitVector(filename='message.txt')
keyBitVector_64_Bits = BitVector(filename='key.txt').read_bits_from_file(64)
oldBitString = Encryption()
Total = 0

'''
	Running for first 7 bits change in key sequentially
'''
for i in range(0,8):
    fullMessageBitVectors = BitVector(filename='message.txt')
    keyBitVector_64_Bits = BitVector(filename='key.txt').read_bits_from_file(64)
    keyBitVector_64_Bits[i] = not(keyBitVector_64_Bits[i])
    newBitString = Encryption()
    Total += calculateChanges(oldBitString,newBitString)

Average = Total / 7
print "Average No Of Cipher Bits Changed For 7 Choice of Keys = "+ str(Average)
