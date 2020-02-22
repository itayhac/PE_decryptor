import binascii
import random
import string
from functools import partial
# filename = '/home/itay/Downloads/AE/AssemblyEdit 2.0 LITE EDITION.exe'
filename = '/home/itay/Downloads/Heroes of Might and Magic III Complete/Heroes3.exe'
FILE_SHOW_SIZE = 150
KEY_MAX_SIZE = 30
CHUNCK_SIZE = 1024
ENCRYPTED_FILE = 'encrypted.exe'
KEY = ''
KEY_SIZE = random.randint(1,KEY_MAX_SIZE)

def random_string_digits(stringLength=KEY_SIZE):
    global KEY
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    KEY = ''.join(random.choice(lettersAndDigits) for i in range(stringLength))
    KEY = KEY.encode()

def xor(data, key):
    key_size = len(key)
    result = bytearray()
    i = 0
    for h in data:
        result.append((h ^ key[i%key_size]))
        i = i+1
    bytes_result = bytes(result)
    return bytes_result

#Generatign random string key, up to limit of 30 bytes (Configurable)
random_string_digits()
print ('The key is: '+str(KEY))


with open(filename, 'rb') as read_object:
    with open(ENCRYPTED_FILE, 'wb') as write_object:
        # print(encrypted_file[0:CHUNCK_SIZE])
        for chunk in iter(partial(read_object.read, CHUNCK_SIZE), b''):
            encrypted_file = xor(chunk, key=KEY)
            write_object.write(encrypted_file)