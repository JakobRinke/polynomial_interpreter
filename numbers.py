import itertools
flatten_iter = itertools.chain.from_iterable
import math
from fraction import Fraction

def factors(n):
    return set(flatten_iter((i, n//i)
                for i in range(1, int(n**0.5)+1) if n % i == 0))

def least_common_multiplier(rationals):
    denominators = [Fraction(r).denominator for r in rationals]

    lcm = denominators[0]
    for d in denominators[1:]:
        lcm = lcm // math.gcd(lcm, d) * d

    return lcm

sign = lambda x: (1, -1)[x<0]