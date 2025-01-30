import logging
from math import log, isqrt

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
    
        limit = self._nth_prime_limit(n)
        self.logger.debug(f"Calculating the {n}th prime number with a limit of {limit}")
    
        chunk_size = min(limit, 10000000)
        current_position = 0
        primes = []
        while (limit > current_position):
            # initialize the sieve chunk
            sieve = [True] * chunk_size
            sieve[0] = False # first element in chunk of even size is never prime

            # 1 isn't prime
            if (current_position == 0):
                sieve[1] = False

            # mark all multiples of previously found primes in the current chunk as not prime
            for prime in primes:
                for multiple in range((current_position // prime + 1) * prime, chunk_size + current_position, prime):
                    sieve[multiple - current_position] = False

            # from current position to current chunk limit or sqrt(limit)
            for current in range(max(current_position, 2), min(isqrt(limit) + 1, chunk_size + current_position)):
                # if i is prime
                if sieve[current - current_position]:
                    # mark all multiples of i as not prime (starting at i^2)
                    for multiple in range(current * current, chunk_size + current_position, current):
                        sieve[multiple - current_position] = False

            # assemble all primes from the sieve chunk (`True` values)
            chunk_primes = [num + current_position for num, is_prime in enumerate(sieve) if is_prime]
            primes.extend(chunk_primes)

            current_position += chunk_size

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