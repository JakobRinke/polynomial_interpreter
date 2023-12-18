import itertools
flatten_iter = itertools.chain.from_iterable

def factors(n):
    return set(flatten_iter((i, n//i)
                for i in range(1, int(n**0.5)+1) if n % i == 0))