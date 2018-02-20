from BitVector import *
from Tables import *

Keys = {i: None for i in range(16)}
data = ""

with open('cipher.txt', 'r') as myfile:
    data=myfile.read().replace('\n', '')

fullCipherBitVectors = BitVector(filename='output.bits')
keyBitVector_64_Bits = BitVector(filename='key.txt').read_bits_from_file(64)
#keyBitVector_64_Bits = BitVector(hexstring = "0E329232EA6D0D73")
finalCipherTextInASCII = ""

def sBox(CipherBitVector_48_Bits):
    iteration = 0
    cipher_32_Bits = ""
    for i in range(0,len(CipherBitVector_48_Bits),6):
        rowBinary = str(CipherBitVector_48_Bits[i])+str(CipherBitVector_48_Bits[i+5])
        rowDecimal = int(rowBinary,2)
        colBinary = str(CipherBitVector_48_Bits[i+1:i+5])
        colDecimal = int(colBinary,2)
        cipher_32_Bits += str("{0:04b}".format(S_BOX[iteration][rowDecimal][colDecimal]))
        iteration += 1
    return BitVector(bitstring = cipher_32_Bits).permute(S_BOX_PERMUTE_TABLE_ORIGINAL_MODIFIED)

def generateKeysAndStore():
    keyBitVector_56_Bit = keyBitVector_64_Bits.permute(PC_1_ORIGINAL_MODIFIED)
    [leftKeyBitVector_28_Bits, rightKeyBitVector_28_Bits] = keyBitVector_56_Bit.divide_into_two()
    for currentIteration in range(0,16):
        leftKeyBitVector_28_Bits << ITERATION_AND_SHIFTS[currentIteration]
        rightKeyBitVector_28_Bits << ITERATION_AND_SHIFTS[currentIteration]
        newKeyBitVector_56_Bits = leftKeyBitVector_28_Bits + rightKeyBitVector_28_Bits
        Keys[15-currentIteration] = newKeyBitVector_56_Bits.permute(PC_2_ORIGINAL_MODIFIED)

def f(rightCipherBitVector_32_Bits,keyBitVector_48_Bits):
    rightCipherBitVector_48_Bits = rightCipherBitVector_32_Bits.permute(E_BOX_PERMUTATION_ORIGINAL)
    newrightCipherBitVector_48_Bits = rightCipherBitVector_48_Bits ^ keyBitVector_48_Bits
    result = sBox(newrightCipherBitVector_48_Bits)
    return result

def returnPadding():
    binString = ""
    for i in range(0,32):
        binString += "0"
    padding = str("0000110100001010") + binString;
    return padding



generateKeysAndStore()
while fullCipherBitVectors.more_to_read:
    singleCipherBitVector_64_Bits = fullCipherBitVectors.read_bits_from_file(64)
    lenOfCipherText = len(singleCipherBitVector_64_Bits)
    permutedSingleCipherBitVector_64_Bits = singleCipherBitVector_64_Bits.permute(INITIAL_PERMUTATION_64_BITS_MODIFIED)
    [oldLeftCipherBitVector_32_Bits,oldRightCipherBitVector_32_Bits] = permutedSingleCipherBitVector_64_Bits.divide_into_two()
    for currentIteration in range(0, 16):
        keyBitVector_48_Bits = Keys[currentIteration]
        newLeftCipherBitVector_32_Bits = oldRightCipherBitVector_32_Bits
        newRightCipherBitVector_32_Bits = oldLeftCipherBitVector_32_Bits ^ f(oldRightCipherBitVector_32_Bits,keyBitVector_48_Bits)
        oldLeftCipherBitVector_32_Bits = newLeftCipherBitVector_32_Bits
        oldRightCipherBitVector_32_Bits = newRightCipherBitVector_32_Bits

    reversedMessageBitVector_64_Bits = newRightCipherBitVector_32_Bits + newLeftCipherBitVector_32_Bits  #Reversing
    finalMessageBitVector_64_Bits = reversedMessageBitVector_64_Bits.permute(INVERSE_INITIAL_PERMUTATION_64_BITS_MODIFIED)
    cipherTextInAscii = finalMessageBitVector_64_Bits.get_bitvector_in_ascii()
    finalCipherTextInASCII += cipherTextInAscii


print "+++++++++++++++++++++ Final Full Plain Text ASCII Representation ++++++++++++++++++++++++++++++++++++++++++++"
print finalCipherTextInASCII

