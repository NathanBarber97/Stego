import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from bitstring import ConstBitStream

def hidemsg(coverImg, hiddenMsg, header, password):
    fullMsg = b"@header" + header + b"@message" + hiddenMsg + b"@end"
    cipherText = encrypt(fullMsg, password.encode()) + b'@!590@'
    bitstream = ConstBitStream(bytes=cipherText)
    stegoImg = b""
    byteCount  = 0
    for byte in coverImg:
        byteCount += 1
        if byteCount < bitstream.length:
            newBit = bitstream.read("bits:1").bin
            newByte = setbit(byte, newBit)
            stegoImg += newByte.to_bytes(1, byteorder='big')
        else:
            stegoImg += byte.to_bytes(1, byteorder='big')

    return stegoImg

def extractmsg(stegoImg, password):
    hiddenBits = ''
    for byte in stegoImg:
        hiddenBits += bin(byte)[-1]
    encryptedMsg = convertBitstoBytes(hiddenBits)
    index = encryptedMsg.find('@!590')
    if index == -1:
        print ("@!590 not found")
    hiddenBytes = (decrypt(encryptedMsg[:index].encode(), password.encode()))
    hiddenMsg = hiddenBytes.decode("utf-8","replace")
    headerIndex = hiddenMsg.find('@header')
    messageIndex = hiddenMsg.find('@message')
    endIndex = hiddenMsg.find('@end')
    return hiddenMsg[headerIndex + 7 : messageIndex], hiddenBytes[messageIndex + 8 : endIndex]

def convertBitstoBytes(bits):
    byteChunks = [bits[i:i+8] for i in range(0, len(bits), 8)]
    bytes = ''
    for byteChunk in byteChunks:
        bytes += chr(int(byteChunk, 2))
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
