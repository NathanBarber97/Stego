import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from bitstring import ConstBitStream

# ----------------------------------------------------------------------------------------------------------------------
# The hidemsg function hides a header and a hidden message in the lowest bit of the bytes of an image, after
# encrypting them
#
# Params:
# coverImg - an array of bytes that represents an image
# hiddenMsg - an array of bytes that represents a hidden message
# header - a header describing the hidden message
# password - the password used to encrypt the message
#
# Returns:
# hidemsg returns an array of bytes that represents a new image with the message hidden inside
# ----------------------------------------------------------------------------------------------------------------------
def hidemsg(coverImg, hiddenMsg, header, password):
    #add separators to message and encrypt it
    fullMsg = b"@header" + header + b"@message" + hiddenMsg + b"@end"
    cipherText = encrypt(fullMsg, password.encode()) + b'@!590@'
    #turn the encrypted message into bits
    bitstream = ConstBitStream(bytes=cipherText)
    #new image bytes
    stegoImg = b""
    byteCount  = 0
    for byte in coverImg:
        byteCount += 1
        #make sure there are still bits to store
        if byteCount < bitstream.length:
            newBit = bitstream.read("bits:1").bin
            newByte = setbit(byte, newBit)
            stegoImg += newByte.to_bytes(1, byteorder='big')
        else:
            stegoImg += byte.to_bytes(1, byteorder='big')

    return stegoImg

# ----------------------------------------------------------------------------------------------------------------------
# The extractmsg function extracts the header and the hidden message from the lowest bit of the bytes of an image, and
# decrypts them
#
# Params:
# stegoImg - an array of bytes that represents an image that has a hidden message
# password - the password used to decrypt the message
#
# Returns:
# extractmessage returns a string containing the header and an array of bytes that represents the hidden message
# ----------------------------------------------------------------------------------------------------------------------
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

# ----------------------------------------------------------------------------------------------------------------------
# The convertBitstoBytes function converts an array of bits into an array of bytes
#
# Params:
# bits - the array of bits to be converted
#
# Returns:
# convertBitstoBytes returns the array of bytes
# ----------------------------------------------------------------------------------------------------------------------
def convertBitstoBytes(bits):
    byteChunks = [bits[i:i+8] for i in range(0, len(bits), 8)]
    bytes = ''
    for byteChunk in byteChunks:
        bytes += chr(int(byteChunk, 2))
    return bytes

# ----------------------------------------------------------------------------------------------------------------------
# The setbit function sets the lowest bit of a byte and returns the new byte
#
# Params:
# byte - the old byte that is to be modified
# bit - the new bit to be stored in the lowest bit of the byte
#
# Returns:
# setbit returns the byte with the last bit modified
# ----------------------------------------------------------------------------------------------------------------------
def setbit(byte, bit):
    newByte = list(bin(byte))
    newByte[-1] = bit
    return int(''.join(newByte), 2)

# ----------------------------------------------------------------------------------------------------------------------
# The encrypt function takes in a message and encrypts using the Fernet encryption algorithm from the cryptography
# package
#
# Params:
# hiddenMsg - the plaintext to be encrypted (in bytes)
# password - the password used to encrypt the message (in bytes)
#
# Returns:
# encrypt returns an array of bytes that represents the encrypted message
# ----------------------------------------------------------------------------------------------------------------------
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

# ----------------------------------------------------------------------------------------------------------------------
# The decrypt function takes in ciphertext and decrypts it using the Fernet encryption algorithm from the cryptography
# package
#
# Params:
# ciphertext - the ciphertext to be decrypted (in bytes)
# password - the password used to decrypt the message (in bytes)
#
# Returns:
# decrypt returns an array of bytes that represents the decrypted message
# ----------------------------------------------------------------------------------------------------------------------
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
