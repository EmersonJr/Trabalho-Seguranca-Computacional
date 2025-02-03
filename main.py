from rsa import Rsa
from pickle import dumps, loads
import hashlib
import base64


if __name__ == "__main__":
    
    message = input("Insira uma mensagem a ser encriptada: ").encode()

    rsa = Rsa()

    # I-a) Generating public and private key (P and Q prime numbers with 1024 bits)
    public_key, private_key = rsa.gen_keys()

    print("Chave Pública --> ", public_key)
    print("Chave Privada --> ", private_key)
    #I -b) Encrypting and decrypting message 
    encrypted_message = rsa.OAEP_encrypt(message, public_key)
    print("Mensagem encriptada --> ", encrypted_message)
    decrypted_message = rsa.OAEP_decrypt(encrypted_message, private_key)
    print("Mensagem decriptada --> ", decrypted_message)


    # Assinatura - > 

    # II-1) Calculating the Hash from the messages

    msg_hash = hashlib.sha3_256(message).digest()
    
    print("Hash gerada pelo sha3 --> ", msg_hash)

    # II-2) Encrypting the calculated hash using the OEAP-RSA algorithm

    authentic_keys = rsa.gen_keys()

    encoded_msg_hash = rsa.OAEP_encrypt(msg_hash, authentic_keys[0])
    print("Hash da mensagem encriptado --> ", encoded_msg_hash)
    # II-3) Encoding the encrypted hash using the BASE64 format

    msg_hash_encoded_b64 = base64.b64encode(dumps(encoded_msg_hash))

    print("Hash codificada em BASE64 --> ", msg_hash_encoded_b64)

    # III) Verificação

    # III-1) Decoding using base64

    hash_msg_decoded_b64 = base64.b64decode(msg_hash_encoded_b64)
    msg_hash_encrypted = loads(hash_msg_decoded_b64)
    print("Hash decodificada --> ", msg_hash_encrypted)

    # III-2) Decrypting the message hash

    decrypt_msg_hash = rsa.OAEP_decrypt(msg_hash_encrypted, authentic_keys[1])
    print("Hash da mensagem decriptado --> ", decrypt_msg_hash)
    # III-3) Testing the original hash with another message hash

    another_message = "Não sei o que escrever".encode()
    
    another_message_hash = hashlib.sha3_256(another_message).digest()

    if another_message_hash == msg_hash:
        print("Autenticação realizada com sucesso!!")
    else:
        print("A autenticação falhou!!")