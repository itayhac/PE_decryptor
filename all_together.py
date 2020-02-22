from collections import Counter
filename = '/home/itay/Downloads/AE/AssemblyEdit 2.0 LITE EDITION.exe'
# filename = '/home/itay/Downloads/Heroes of Might and Magic III Complete/Heroes3.exe'
KEY = b'gakfuticmbpaicjgi'
KEY_SIZE = len(KEY)
PE_FILE_HEADER_SIZE = 64
FILE_SHOW_SIZE = 150

def find_longest_sub_sequence(data, rep_min_len=KEY_SIZE):
    counter = Counter()
    for i in range(0,len(data)-KEY_SIZE,KEY_SIZE):
        input = bytes(data[i:i+KEY_SIZE])
        counter[input] +=1
    suggested_key = counter.most_common(1)[0]
    print (suggested_key[0])
    return (suggested_key[0])

with open(filename, 'rb') as f:
    original_hex_file = f.read()

def xor(data, key):
    key_size = len(key)
    result = bytearray()
    i = 0
    for h in data:
        result.append((h ^ key[i%key_size]))
        i = i+1
    bytes_result = bytes(result)
    return bytes_result


print (original_hex_file[0:FILE_SHOW_SIZE])
encrypted_file = xor(original_hex_file, key=KEY)
print (encrypted_file[0:FILE_SHOW_SIZE])
suggested_key = find_longest_sub_sequence(encrypted_file)
decrypted_file = xor(encrypted_file, key=suggested_key)
print (decrypted_file[0:FILE_SHOW_SIZE])

print (decrypted_file == original_hex_file)