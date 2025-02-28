from Encrypt import hybrid_encrypt
from Decrypt import hybrid_decrypt
from IVsKeys import generateKey, FetchKey
import threading

def HybridCrypt():
    # Generate encryption key
    key = generateKey()  # This should return an integer (e.g., 12345)
    
    # Start encryption thread
    t1 = threading.Thread(target=hybrid_encrypt, args=("input.txt", "encrypted_output.enc", key,))
    
    # Start encryption
    t1.start()
    
    # Wait for thread to finish
    t1.join()
    
    print("Encryption Completed.")

def HybridDeCrypt():
    # Fetch decryption key
    key = FetchKey()  # This should return the same integer used for encryption

    # Start decryption thread
    t1 = threading.Thread(target=hybrid_decrypt, args=("encrypted_output.enc", "decrypted_output.txt", key,))

    # Start decryption
    t1.start()
    
    # Wait for thread to finish
    t1.join()

    print("Decryption Completed.")
