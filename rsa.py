from gen_primes import Gen_Primes
import hashlib
import os
import struct

class Rsa:

    def __init__(self):
        
        self.generator = Gen_Primes()
        self.hash256 = hashlib.sha256
        self.k = 128
        self.h_len = self.hash256().digest_size

    def gen_keys(self):

        p = self.generator.gen()
        q = self.generator.gen()

        mod = p*q

        euler_totient = (p-1)*(q-1)

        encrypt_exp = 65587

        # Calculating the d = e^(-1) % N using the euler theorem
        # e^(-1) = e^(phi(N) - 1) % N

        decrypt_exp = pow(encrypt_exp, euler_totient-1, mod)

        pub_key = [encrypt_exp, mod]
        priv_key = [decrypt_exp, mod]

        return(pub_key, priv_key)
    
    def rsa_encrypt(self, message, pub_key):
        
        '''

        Params:

        pub_key: list of two integers "e" and "n"
        message: Message represented as a list of integers

        return:
        
        CypherTxt: list of integers. the result from the encryption
        the encryption format is:

        C = M^e mod n

        '''
        cypher_txt = []
        for num in message:

            cypher_txt.append(pow(num, pub_key[0], pub_key[1]))
        
        return cypher_txt
    
    def rsa_decrypt(self, cypher, priv_key):
        
        '''

        Params:

        priv_key: list of two integers "d" and "n"
        ypher:  cypher text represented as a list of integers

        return:
        
        plain_txt: list of integers. the result from the Decryption
        the encryption format is:

        M = C^d mod n

        '''
        plain_txt = []
        for num in cypher:

            plain_txt.append(pow(num, priv_key[0], priv_key[1]))
        
        return plain_txt
    

    def create_data_block(self, l_hash, message):

        ps = bytearray()

        for _ in range(self.k - len(message) - (2*self.h_len) - 2):
            ps.append(0)
        
        return bytearray(l_hash + ps + b'\x01' + message)

    def mgf1(self, seed, mask_len, hash_func):
        
        T = bytearray()

        for i in range((mask_len + self.h_len - 1) // self.h_len):
            c = struct.pack(">I", i)
            T += hash_func(seed + c).digest()

        return bytearray(T[:mask_len])

    def OAEP_encrypt(self, message, pub_key, label = ""):
        
        if len(message) > self.k - 2 * self.h_len - 2:
            raise NameError("Message is too long")

        label = label.encode()

        l_hash = self.hash256(label).digest()

        data = self.create_data_block(l_hash,message)

        seed = bytearray(os.urandom(self.h_len))

        data_mask = self.mgf1(seed, self.k - self.h_len - 1, self.hash256)

        for i in range(len(data)):
            data[i] = data[i] ^ data_mask[i]

        data = bytes(data)

        seed_mask = self.mgf1(data,self.h_len,self.hash256)

        for i in range(len(seed)):
            seed[i] = seed[i] ^ seed_mask[i]
        
        seed = bytes(seed)

        encoded_message = b'\x00' + seed + data

        return self.rsa_encrypt(encoded_message, pub_key)
    
    
    def OAEP_decrypt(self, encoded_message, priv_key, label = ""):
    

        encoded_message = self.rsa_decrypt(encoded_message,priv_key)

        if len(encoded_message) != self.k:
            raise NameError("Encoded message has wrong length")
        
        label = label.encode()

        seed = bytearray(encoded_message[1:self.h_len+1])
        data = bytearray(encoded_message[self.h_len+1:])

        seed_mask = self.mgf1(data, self.h_len, self.hash256)

        for i in range(len(seed)):
            seed[i] = seed[i] ^seed_mask[i]

        data_mask = self.mgf1(seed, self.k-self.h_len-1, self.hash256)

        for i in range(len(data)):
            data[i] = data[i] ^ data_mask[i]

        test_l = self.hash256(label).digest()

        l_hash = data[:self.h_len]

        if l_hash != test_l:
            raise NameError("Incorrect label has")
        
        message_size = self.h_len + data[self.h_len].find(b'\x01') + 1
        message = data[message_size:]

        return message
