import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from bitstring import ConstBitStream
from bitstring import BitArray
from binascii import a2b_hex, b2a_uu

def hidemsg(coverImg, hiddenMsg, header, password):
    fullMsg = b"@header" + header + b"@message" + hiddenMsg + b"@end"
    cipherText = encrypt(fullMsg, password.encode()) + b'@!590@'
    #print(cipherText)
    #cipherText = fullMsg
    if len(cipherText)*8 > len(coverImg):
        print("hidden too big!!!")
    bitstream = ConstBitStream(bytes=cipherText)
    stegoImg = b""
    byteCount  = 0
    for byte in coverImg:
        byteCount += 1
        if byteCount < bitstream.length:
            newBit = bitstream.read("bits:1").bin
            # print("new bit" + str(newBit))
            newByte = setbit(byte, newBit)
            # print("new byte" + str(bytes(newByte)))
            stegoImg += newByte.to_bytes(1, byteorder='big')
            # print("stegoImg" + str(stegoImg))
        else:
            stegoImg += byte.to_bytes(1, byteorder='big')

    return stegoImg

def extractmsg(stegoImg, password):
    hiddenBits = ''
    for byte in stegoImg:
        hiddenBits += bin(byte)[-1]
    #print(hiddenBits)
    encryptedMsg = convertBitstoBytes(hiddenBits)
    index = encryptedMsg.find('@!590')
    if index == -1:
        print ("@!590 not found")
    #print(encryptedMsg[:index].encode())
    hiddenBytes = (decrypt(encryptedMsg[:index].encode(), password.encode()))
    hiddenMsg = hiddenBytes.decode("utf-8","replace")
    headerIndex = hiddenMsg.find('@header')
    messageIndex = hiddenMsg.find('@message')
    endIndex = hiddenMsg.find('@end')
    return hiddenMsg[headerIndex + 7 : messageIndex], hiddenBytes[messageIndex + 8 : endIndex]

def convertBitstoBytes(bits):
    byteChunks = [bits[i:i+8] for i in range(0, len(bits), 8)]
    bytes = ''
    #print(byteChunks)
    for byteChunk in byteChunks:
        bytes += chr(int(byteChunk, 2))
    #print(bytes)
    return bytes

def setbit(byte, bit):
    newByte = list(bin(byte))
    newByte[-1] = bit
    return int(''.join(newByte), 2)


def encrypt(hiddenMsg, password):
    salt = b'?%U;\x97\xd8%\x8c\x08\xae\xdeL\xae\xba\xa5M'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))
    encrypter = Fernet(key)
    token = encrypter.encrypt(hiddenMsg)
    return token

def decrypt(cipherText, password):
    salt = b'?%U;\x97\xd8%\x8c\x08\xae\xdeL\xae\xba\xa5M'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))
    encrypter = Fernet(key)
    return encrypter.decrypt(cipherText)
