import random as rnd
from millerrabin import MillerRabin

class Gen_Primes:

    def __init__(self):

        self.rng = rnd.SystemRandom()
        self.Miller_Rabin = MillerRabin()
    
    def gen(self):

        while True:

            candidato_primo = ((self.rng.randrange(1 << 1024 - 1, 1 << 1024) << 1)) + 1

            if self.Miller_Rabin.primo(candidato_primo):
                return candidato_primo