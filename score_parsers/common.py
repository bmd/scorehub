from itertools import izip, chain, repeat


def group(n, iterable, padvalue=None):
    return izip(*[chain(iterable, repeat(padvalue, n-1))]*n)
