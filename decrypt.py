#Author: Itay hacohen

from collections import Counter, OrderedDict, defaultdict
from functools import partial
ENCRYPTED_FILE = 'encrypted.exe'
DECRYPTED_FILE = 'decrypred.exe'
FILE_SHOW_SIZE = 150
KEY_MAX_SIZE = 35
CHUNCK_SIZE = 1024
FIRST_2_BYTES_PE_HEADER = b'MZ'
counter = Counter()
suggested_keys = []

def get_repeated_bytes(bytes):
    string = bytes.decode()
    for x in range(1, len(string)):
        substring = string[:x]
        if substring * (len(string)//len(substring))+(substring[:len(string)%len(substring)]) == string:
            return substring.encode()
    return string.encode()

def find_longest_sub_sequence(data):
    global suggested_keys
    counter = Counter()
    for key_size in range (1, KEY_MAX_SIZE):
        for i in range(0,CHUNCK_SIZE,key_size ):
            input = bytes(data[i:i+key_size])
            counter[input] += 1
    ordered_keys = OrderedDict(sorted(counter.items(), key=lambda t: len(t[0]), reverse=True))
    suggested_keys = [k for k,v in ordered_keys.items() if v>1]
    return suggested_keys

def xor(data, key):
    key_size = len(key)
    result = bytearray()
    i = 0
    for h in data:
        result.append((h ^ key[i%key_size]))
        i = i+1
    bytes_result = bytes(result)
    return bytes_result

def decrypt(data):
    for key in suggested_keys:
        original_key = get_repeated_bytes(key)
        suggested_solution = xor(data[0:2], original_key)
        if suggested_solution == FIRST_2_BYTES_PE_HEADER:
            print ('The suggested key is: '+str(original_key))
            return original_key

with open(ENCRYPTED_FILE, 'rb') as read_object:
    first_chunk = read_object.read(CHUNCK_SIZE)
    find_longest_sub_sequence(first_chunk)
    key = decrypt(first_chunk)
    print(xor(first_chunk, key))

with open(ENCRYPTED_FILE, 'rb') as read_object:
    with open(DECRYPTED_FILE, 'w+b') as write_object:
        for chunk in iter(partial(read_object.read, CHUNCK_SIZE), b''):
            decrypted_chunk = xor(chunk, key)
            write_object.write(decrypted_chunk)

