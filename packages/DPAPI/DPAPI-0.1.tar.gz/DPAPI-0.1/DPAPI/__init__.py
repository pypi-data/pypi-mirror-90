# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

# Import modules
from ctypes import (
        windll, cdll,
        wintypes, Structure,
        byref, POINTER,
        c_char, c_buffer,
    )


# This flag is used for remote situations where the user interface (UI) is not an option. 
# When this flag is set and UI is specified for either the protect or unprotect operation, 
# the operation fails and GetLastError returns the ERROR_PASSWORD_RESTRICTION code.
CRYPTPROTECT_UI_FORBIDDEN = 0x01

""" Data blob structure """
class __DATA_BLOB(Structure):
    _fields_ = [
            ("cbData", wintypes.DWORD), 
            ("pbData", POINTER(c_char))
        ]

""" Get data """
def __GetData(blobOut: bytes) -> bytes:
    cbData = int(blobOut.cbData)
    pbData = blobOut.pbData
    buffer = c_buffer(cbData)
    cdll.msvcrt.memcpy(buffer, pbData, cbData)
    windll.kernel32.LocalFree(pbData)
    return buffer.raw

""" Protect byte array """
def CryptProtectData(plainText: bytes, entropy=b'') -> bytes:
    bufferIn = c_buffer(plainText, len(plainText))
    blobIn = __DATA_BLOB(len(plainText), bufferIn)
    bufferEntropy = c_buffer(entropy, len(entropy))
    blobEntropy = __DATA_BLOB(len(entropy), bufferEntropy)
    blobOut = __DATA_BLOB()

    if windll.crypt32.CryptProtectData(byref(blobIn), None, byref(blobEntropy),
                       None, None, CRYPTPROTECT_UI_FORBIDDEN, byref(blobOut)):
        return __GetData(blobOut)
    return b''

""" Unprotect byte array """
def CryptUnprotectData(cipherText: bytes, entropy=b'') -> bytes:
    bufferIn = c_buffer(cipherText, len(cipherText))
    blobIn = __DATA_BLOB(len(cipherText), bufferIn)
    bufferEntropy = c_buffer(entropy, len(entropy))
    blobEntropy = __DATA_BLOB(len(entropy), bufferEntropy)
    blobOut = __DATA_BLOB()
    if windll.crypt32.CryptUnprotectData(byref(blobIn), None, byref(blobEntropy), None, None,
                              CRYPTPROTECT_UI_FORBIDDEN, byref(blobOut)):
        return __GetData(blobOut)
    return b''
