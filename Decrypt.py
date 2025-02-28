import os

def hybrid_decrypt(input_file, key, iv):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    with open(input_file, "rb") as f:
        encrypted_data = f.read()
    
    print(f"Decrypting file: {input_file}")
    decrypted_data = custom_decrypt_function(encrypted_data, key, iv)

    output_file = f"decrypted_{input_file}"
    with open(output_file, "wb") as f:
        f.write(decrypted_data)
    
    print(f"Decrypted file saved as {output_file}")

def custom_decrypt_function(data, key, iv):
    # Implement your own decryption logic here
    return data[::-1]  # Simple reverse (replace with real decryption algorithm)
