from .gen_primes import Gen_Primes

class Rsa:

    def __init__(self):
        
        self.generator = Gen_Primes()

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
        
        CypherTxt: list of integers. the result of the encryption
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
        
        plain_txt: list of integers. the result of the Decryption
        the encryption format is:

        M = C^d mod n

        '''
        plain_txt = []
        for num in cypher:

            plain_txt.append(pow(num, priv_key[0], priv_key[1]))
        
        return plain_txt