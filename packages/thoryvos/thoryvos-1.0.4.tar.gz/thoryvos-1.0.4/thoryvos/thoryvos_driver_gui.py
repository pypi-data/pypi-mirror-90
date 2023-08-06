"""throyvos Driver Code."""
# Importing backend libraries
from .thoryvos_encoder import write_data
from .thoryvos_crypto import Encrypt, Decrypt
from .thoryvos_stego import Stego
from .thoryvos_transfer import upload, download, verify
from Crypto.Util.Padding import pad


# Importing Dependencies
from os.path import exists, splitext
from os import remove


def cleanup(*args, **kwargs):
    """Delete created files in case of error."""
    for file in args:
        if exists(file):
            remove(file)
    for file in kwargs:
        if exists(file):
            remove(file)


def get_extension(filename):
    """Return extension padded tp 8 bytes in binary format."""
    extension = splitext(filename)[1].encode()
    return pad(extension, 16)


def encryptor(infile: str, outfile: str, password: str, mode: str) -> int:
    """Encryption Driver for thoryvos backend."""
    enc = Encrypt(infile)

    if mode.upper() == 'AES':
        encrypted_data = enc.AES(password)
    elif mode.upper() == 'DES':
        encrypted_data = enc.DES(password)
    elif mode.upper() == 'SALSA20':
        encrypted_data = enc.Salsa20(password)
    else:
        return 2

    if not encrypted_data:
        return 3

    write_data(get_extension(infile) + encrypted_data, outfile)
    return 0


def decryptor(infile: str, outfile: str, password: str, mode: str) -> int:
    """Decryption Driver for thoryvos backend."""

    dec = Decrypt(infile)

    if mode.upper() == 'AES':
        decrypted_data = dec.AES(password)
    elif mode.upper() == 'DES':
        decrypted_data = dec.DES(password)
    elif mode.upper() == 'SALSA20':
        decrypted_data = dec.Salsa20(password)
    else:
        return 2

    if not decrypted_data:
        cleanup(outfile)
        return 3

    if not outfile.endswith(dec.extension):
        outfile += dec.extension
    write_data(decrypted_data, outfile)
    return 0


def anon_upload(infile: str):
    """File Transfer Driver for throyvos backend."""
    if exists(infile):
        URL = upload(infile)
        return URL
    return 5


def anon_download(url: str):
    """File Transfer Driver for throyvos backend."""
    if verify(url):
        location = download(url)
        return location
    return 6


def hide_data(infile: str, outfile: str, datafile: str, lsb=None):
    """Steganography Hiding Driver for throyvos backend."""
    if not infile.endswith('.wav'):
        return 4

    if not outfile.endswith('.wav'):
        return 4

    try:
        lsb = int(lsb)
    except TypeError:
        lsb = None

    steganographer = Stego(infile, lsb)
    lsb, datasize = steganographer.hide(datafile, outfile)

    if not datasize:
        cleanup(outfile)
        return 3

    return (lsb, datasize)


def recover_data(infile: str, outfile: str, lsb: int, nbytes: int):
    """Steganography Retrieval Driver for throyvos backend."""
    if not lsb:
        return 7
    if not nbytes:
        return 8

    if not infile.endswith('.wav'):
        return 4

    try:
        lsb = int(lsb)
    except TypeError:
        lsb = lsb

    steganographer = Stego(infile, lsb)
    if steganographer.recover(outfile, nbytes):
        return 0

    cleanup(outfile)
    return 1


if __name__ == '__main__':
    exit("Driver code cannot be used directly.")
