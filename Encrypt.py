import os

def hybrid_encrypt(input_file, key, iv):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    with open(input_file, "rb") as f:
        data = f.read()
    
    print(f"Encrypting file: {input_file} using custom encryption algorithm")
    encrypted_data = custom_encrypt_function(data, key, iv)

    output_file = f"encrypted_{input_file}"
    with open(output_file, "wb") as f:
        f.write(encrypted_data)
    
    print(f"Encrypted file saved as {output_file}")

def custom_encrypt_function(data, key, iv):
    return data[::-1] 
