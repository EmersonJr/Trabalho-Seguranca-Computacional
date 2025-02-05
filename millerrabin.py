import random as rnd


class MillerRabin:

    def __init__(self):
        self.rng = rnd.SystemRandom()

    
    def possivelmentePrimo(self, base, exp, resto, modulo):
        
        x = pow(base,exp,modulo)

        if x == 1 or x == modulo-1:
            return True


        for i in range(resto):
            x = (x*x)%modulo

            if x == modulo-1:
                return True
            if x == 1:
                return False
            
        return False
        


    def primo(self, numero, iteracoes = 100):
        if numero <= 1:
            return False
        if numero <= 3:
            return True
        if numero%2 == 0 or numero%3 == 0:
            return False
        
        exp, resto = numero-1, 0

        while exp%2 == 0:
            exp //= 2
            resto += 1
        
        for i in range(iteracoes):
            baseParaTeste = self.rng.randrange(2,numero-2)
            
            if self.possivelmentePrimo(baseParaTeste,exp, resto, numero) == False:
                return False
        return True