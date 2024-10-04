def format_private_key(private_key_path):
    with open(private_key_path, 'r') as key_file:
        private_key = key_file.read()
    return private_key.replace('\n', '\\n')

formatted_key = format_private_key('rsa_key.p8')
print(formatted_key)