import os
import secrets
from Crypto.Cipher import AES, ChaCha20
from Crypto.Util.Padding import pad, unpad

class HybridCrypt:
    def __init__(self):
        self.block_key = secrets.token_bytes(16)  # 128-bit AES Key
        self.stream_key = secrets.token_bytes(32)  # 256-bit ChaCha20 Key

    def encrypt_block(self, plaintext):
        cipher = AES.new(self.block_key, AES.MODE_CBC)  # Generate IV automatically
        ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        return cipher.iv + ciphertext  # Prepend IV for later use

    def decrypt_block(self, ciphertext):
        iv = ciphertext[:16]  # Extract IV
        cipher = AES.new(self.block_key, AES.MODE_CBC, iv=iv)
        
        try:
            plaintext = unpad(cipher.decrypt(ciphertext[16:]), AES.block_size)
            return plaintext.decode()
        except ValueError:
            print("❌ ERROR: Incorrect padding! The file may be corrupted or improperly encrypted.")
            return None  # Return None if decryption fails

    def encrypt_stream(self, plaintext):
        cipher = ChaCha20.new(key=self.stream_key)
        ciphertext = cipher.encrypt(plaintext.encode())
        return cipher.nonce + ciphertext

    def decrypt_stream(self, ciphertext):
        nonce = ciphertext[:8]
        cipher = ChaCha20.new(key=self.stream_key, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext[8:])
        return plaintext.decode()

    def encrypt(self):
        os.makedirs("EncryptedSegments", exist_ok=True)

        for i in range(5):
            input_path = os.path.join("Segments", f"{i}.txt")
            output_path = os.path.join("EncryptedSegments", f"{i}.enc")

            with open(input_path, 'r') as f:
                data = f.read()

            encrypted_data = self.encrypt_block(data)

            with open(output_path, 'wb') as f:
                f.write(encrypted_data)

        print("✅ Encryption complete.")

    def decrypt(self):
        os.makedirs("DecryptedSegments", exist_ok=True)

        for i in range(5):
            input_path = os.path.join("EncryptedSegments", f"{i}.enc")
            output_path = os.path.join("Segments", f"{i}.txt")

            with open(input_path, 'rb') as f:
                data = f.read()

            decrypted_data = self.decrypt_block(data)
            if decrypted_data is None:
                print(f"❌ Error decrypting segment {i}. Skipping...")
                continue

            with open(output_path, 'w') as f:
                f.write(decrypted_data)

        print("✅ Decryption complete.")
