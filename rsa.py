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

    def euclides_extendido(self, a, b):
         
        if b == 0:
            return a, 1, 0
        else:
            gcd, num, num1 = self.euclides_extendido(b, a % b)
            return gcd, num1, num - (a // b) * num1
        
    def gen_keys(self):

        p = self.generator.gen()
        q = self.generator.gen()

        mod = p*q

        euler_totient = (p-1)*(q-1)

        encrypt_exp = 65537

        # Calculating the d = e^(-1) % N using extended euclides algo

        decrypt_exp = self.euclides_extendido(encrypt_exp, euler_totient)[1]

        if(decrypt_exp < 0):
            decrypt_exp += euler_totient

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

        #recives the label hash and the message and returns the data block to be encrypted

        ps = bytearray()

        for _ in range(self.k - len(message) - (2*self.h_len) - 2):
            ps.append(0)
        
        return bytearray(l_hash + ps + b'\x01' + message)

    def mgf1(self, seed, mask_len, hash_func):

        # Returns the mask generated by the MGF1 function

        if mask_len > 2**32 * self.h_len: raise ValueError("Mask too long.")
        
        T = bytearray()

        for i in range((mask_len + self.h_len - 1) // self.h_len):
            c = struct.pack(">I", i)
            T += hash_func(seed + c).digest()

        return bytearray(T[:mask_len])

    def OAEP_encrypt(self, message, pub_key, label = ""):
        
        if len(message) > self.k - 2 * self.h_len - 2:
            raise ValueError("Message is too long")

        label = label.encode()

        # hash label with sha256

        l_hash = self.hash256(label).digest()

        #generate padding

        data = self.create_data_block(l_hash,message)

        # generate random seed

        seed = bytearray(os.urandom(self.h_len))

        # generate mask for the message

        data_mask = self.mgf1(seed, self.k - self.h_len - 1, self.hash256)

        # make data = data ^ data_mask to use the mask in the encrypting

        for i in range(len(data)):
            data[i] = data[i] ^ data_mask[i]


        #generate mask for the seed

        seed_mask = self.mgf1(data,self.h_len,self.hash256)

        # make seed = seed ^ seed_mask to use the mask in the encrypting

        for i in range(len(seed)):
            seed[i] = seed[i] ^ seed_mask[i]
        
        seed = bytes(seed)

        # concatenate the padded massage with the modified seed and the modified data

        encoded_message = b'\x00' + seed + data

        #return the message after encrypting with RSA

        return self.rsa_encrypt(list(encoded_message), pub_key)
    
    
    def OAEP_decrypt(self, encoded_message, priv_key, label = ""):

        
        # decrypt the RSA

        encoded_message = self.rsa_decrypt(list(encoded_message),priv_key)


        if len(encoded_message) != self.k:
            raise ValueError("Encoded message has wrong length")
        
        label = label.encode()

        # split the encoded message

        seed = bytearray(encoded_message[1:self.h_len+1])
        data = bytearray(encoded_message[self.h_len+1:])

        # generate the seed_mask that was used

        seed_mask = self.mgf1(data, self.h_len, self.hash256)

        #undo the XOR between seed and seed_mask aplying seed ^ seed_mask ^ seed_mask

        for i in range(len(seed)):
            seed[i] = seed[i] ^seed_mask[i]


        #generate the data mask

        data_mask = self.mgf1(seed, self.k-self.h_len-1, self.hash256)


        # undo the XOR between seed and seed_mask aplying seed ^ seed_mask ^ seed_mask

        for i in range(len(data)):
            data[i] = data[i] ^ data_mask[i]

        # hash the label to make sure the label used is correct

        test_l = self.hash256(label).digest()

        l_hash = data[:self.h_len]

        if l_hash != test_l:
            raise ValueError("Incorrect label hash")
        
        #split the message correctly
        
        message_size = self.h_len + data[self.h_len:].find(b'\x01') + 1
        message = data[message_size:]

        return message
