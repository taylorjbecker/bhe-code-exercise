import logging
from math import log

class Sieve:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def nth_prime(self, n: int) -> int:
        """
        Calculate the Nth prime number (0-indexed from 2) using the Sieve of Eratosthenes
        See algorithm: https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
        """

        if n < 0:
            raise IndexError("n must be a non-negative integer")
    
        limit = self.__nth_prime_limit(n)
        self.logger.debug(f"Calculating the {n}th prime number with a limit of {limit}")
    
        # initialize the sieve
        sieve = [True] * limit
        sieve[0] = sieve[1] = False # 0 and 1 aren't prime

        # from 2 to sqrt(limit)
        for i in range(2, int(limit ** 0.5) + 1):
            # if i is prime
            if sieve[i]:
                # mark all multiples of i as not prime (starting at i^2)
                for multiple in range(i * i, limit, i):
                    sieve[multiple] = False

        # assemble all primes from the sieve (`True` values)
        primes = [num for num, is_prime in enumerate(sieve) if is_prime]

        # log the primes found, within some reasonable limit
        if (n < 100):
            self.logger.debug(f"Primes found: {primes}")
        
        return primes[n]
    
    def _nth_prime_limit(self, n: int) -> int:
        """
        Estimate the upper limit for the nth prime number (0-indexed)

        approx upper bound for a prime via prime number theorem is n(ln(n) + ln(ln(n))) for n > 6
        see also: https://math.stackexchange.com/questions/1270814/bounds-for-n-th-prime
        """
    
        n = n + 1 # adjust to 1-indexed
        return int(n * (log(n) + log(log(n)))) + 1 if n >= 6 else 13