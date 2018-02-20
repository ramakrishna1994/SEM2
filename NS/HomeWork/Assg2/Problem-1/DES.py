'''

@Author : Saradhi Ramakrishna
@ID     : 2017H1030081H
@Description : Below code is practical implementation of DES Encryption and Decryption Procedure.
@Inputs : message and key are read from a file.
@Outputs : Writes output to a binary file for Encryption and prints Plain text to the console for the user for Decryption.

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
	Generating 16 rounds of Keys used for encrypting and decrypting
'''
def generateKeysAndStore():
    keyBitVector_56_Bit = keyBitVector_64_Bits.permute(PC_1_ORIGINAL_MODIFIED)
    [leftKeyBitVector_28_Bits, rightKeyBitVector_28_Bits] = keyBitVector_56_Bit.divide_into_two()
    for currentIteration in range(0,16):
        leftKeyBitVector_28_Bits << ITERATION_AND_SHIFTS[currentIteration]
        rightKeyBitVector_28_Bits << ITERATION_AND_SHIFTS[currentIteration]
        newKeyBitVector_56_Bits = leftKeyBitVector_28_Bits + rightKeyBitVector_28_Bits
        Keys[currentIteration] = newKeyBitVector_56_Bits.permute(PC_2_ORIGINAL_MODIFIED)

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
	A single DES Algorithm procedure for encrypting and decrypting with key interchanging
'''
def DES():
    finalCipherText = ""
    while fullMessageBitVectors.more_to_read:
        singleMessageBitVector_64_Bits = fullMessageBitVectors.read_bits_from_file(64)
        if singleMessageBitVector_64_Bits.length() != 64:
            padding = returnPadding()
            Message = str(singleMessageBitVector_64_Bits)+str(padding[0:64-singleMessageBitVector_64_Bits.length()])
            singleMessageBitVector_64_Bits = BitVector(bitstring=Message)

		# Applying IP table
        permutedSingleMessageBitVector_64_Bits = singleMessageBitVector_64_Bits.permute(INITIAL_PERMUTATION_64_BITS_MODIFIED)
        [oldLeftMessageBitVector_32_Bits,oldRightMessageBitVector_32_Bits] = permutedSingleMessageBitVector_64_Bits.divide_into_two()
        for currentIteration in range(0, 16):
            if user_choice == 1:
                keyBitVector_48_Bits = Keys[currentIteration] # For Encryption
            else:
                keyBitVector_48_Bits = Keys[15-currentIteration] # For Decryption
            newLeftMessageBitVector_32_Bits = oldRightMessageBitVector_32_Bits
            newRightMessageBitVector_32_Bits = oldLeftMessageBitVector_32_Bits ^ f(oldRightMessageBitVector_32_Bits,keyBitVector_48_Bits)
            oldLeftMessageBitVector_32_Bits = newLeftMessageBitVector_32_Bits
            oldRightMessageBitVector_32_Bits = newRightMessageBitVector_32_Bits

        reversedMessageBitVector_64_Bits = newRightMessageBitVector_32_Bits + newLeftMessageBitVector_32_Bits  # Reversing
		# Applyting Inverse Intial Permutation Table
        finalMessageBitVector_64_Bits = reversedMessageBitVector_64_Bits.permute(INVERSE_INITIAL_PERMUTATION_64_BITS_MODIFIED)
        if user_choice == 1:
            finalMessageBitVector_64_Bits.write_to_file(FILEOUT)
            cipherTextInHex = finalMessageBitVector_64_Bits.get_bitvector_in_hex()
            finalCipherText += cipherTextInHex
        if user_choice == 2:
            cipherTextInAscii = finalMessageBitVector_64_Bits.get_bitvector_in_ascii()
            finalCipherText += cipherTextInAscii
    return finalCipherText

while True:
	keyBitVector_64_Bits = BitVector(filename='key.txt').read_bits_from_file(64)
	#keyBitVector_64_Bits = BitVector(hexstring = "0E329232EA6D0D73")
	finalCipherTextInASCII = ""
	finalCipherTextInHEX = ""
	FILEOUT = ""
	Keys = {i: None for i in range(16)}
	fullMessageBitVectors = ""
	generateKeysAndStore()
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	print "\t1.Encryption\n\t2.Decryption\n\t3.Quit"
	user_choice = input("Enter Your Choice : ")
	if user_choice == 1:
		FILEOUT = open('output.bits', 'wb')
		fullMessageBitVectors = BitVector(filename='message.txt')
		print "+++++++++++++++++++++ Final Full Cipher Text In HexaDecimal Representation ++++++++++++++++++++++++++++++++++++++++++++"
	elif user_choice == 2:
		fullMessageBitVectors = BitVector(filename='output.bits')
		print "++++++++++++++++++++++++++++++++ Final Full Plain Text ASCII Representation ++++++++++++++++++++++++++++++++++++++++++++"
	else:
		exit()

	print DES()


