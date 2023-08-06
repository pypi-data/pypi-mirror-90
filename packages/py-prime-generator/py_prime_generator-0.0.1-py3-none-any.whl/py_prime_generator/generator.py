def sieve_of_eratosthenes() -> int:
    """
    An efficient prime number generator.
    :return: All prime numbers
    """
    yield 2

    cache = {}
    n = 3

    while True:
        if p := cache.pop(n, None):
            x = p + n
            while x in cache:
                x += p
            cache[x] = p
        else:
            cache[n * n] = 2 * n
            yield n
        n += 2
