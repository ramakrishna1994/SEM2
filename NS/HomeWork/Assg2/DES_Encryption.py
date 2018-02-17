from BitVector import *
from Tables import *

fullMessageBitVectors = BitVector(filename='message.txt')
keyBitVector_64_Bits = BitVector(filename='key.txt').read_bits_from_file(64)
#keyBitVector_64_Bits = BitVector(hexstring = "0E329232EA6D0D73")
finalCipherTextInASCII = ""
finalCipherTextInHEX = ""
FILEOUT = open('output.bits', 'wb')

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

def returnPadding():
    binString = ""
    for i in range(0,48):
        binString += "0"
    padding = str("0000110100001010") + binString;
    return padding

def f(rightMessageBitVector_32_Bits,keyBitVector_48_Bits):
    rightMessageBitVector_48_Bits = rightMessageBitVector_32_Bits.permute(E_BOX_PERMUTATION_ORIGINAL)
    newrightMessageBitVector_48_Bits = rightMessageBitVector_48_Bits ^ keyBitVector_48_Bits
    result = sBox(newrightMessageBitVector_48_Bits)
    return result



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
    cipherTextInAscii = finalMessageBitVector_64_Bits.get_bitvector_in_ascii()
    cipherTextInHex = finalMessageBitVector_64_Bits.get_bitvector_in_hex()
    finalCipherTextInHEX += cipherTextInHex
    finalMessageBitVector_64_Bits.write_to_file(FILEOUT)

print "+++++++++++++++++++++ Final Full Cipher Text In HexaDecimal Representation ++++++++++++++++++++++++++++++++++++++++++++"
print finalCipherTextInHEX
