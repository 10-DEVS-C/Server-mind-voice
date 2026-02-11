from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import os

def generate_keys():
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Make sure keys directory exists
    if not os.path.exists("keys"):
        os.makedirs("keys")

    # Serialize private key
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open("keys/private.pem", "wb") as f:
        f.write(pem_private)

    # Generate public key
    public_key = private_key.public_key()
    
    # Serialize public key
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open("keys/public.pem", "wb") as f:
        f.write(pem_public)

    print("RSA keys generated in 'keys/' directory.")

if __name__ == "__main__":
    generate_keys()
