"Provides some utilities widely used by other modules"

import bisect
import collections
import collections.abc
import functools
import heapq
import operator
import os.path
import random 
from itertools import chain, combinations 
from statistics import mean 
import numpy as np

#Functions on Sequences and Iterables

def sequence(iterable):
    """Converts iterable to sequence, if it is not already one."""
    return iterable if isinstance (iterable, collections.abc.Sequence) else tuple([iterable])

def remove_all(item, seq):
    """Return a copy of sq ( or string ) with all occurrences of item removed."""
    if isinstance (seq, str):
        return seq.replace(item, '')
    elif isinstance (seq, set):
        rest=  seq.copy()
        rest.remove(item)
        return rest 
    else:
        return [x for x in seq if x != item]
    
def unique(seq):
    """Remove duplicate elements from seq. Assumes hasable element."""
    return list(set(seq))

def count(seq):
    """Count the number of items in sequence that are interpreted as true."""
    return sum(map(bool, seq))

def multimap(items):
    """Given (key, val) pairs. return {key: [val, ...], ...}"""
    result = collections.defaultdict(list)
    for (key, val) in items:
            result[key].append(val)
    return dict(result)

def multimap_items(mmap):
    """Yield all (key, val) pairs stored in the multimap"""
    for (key, vals) in mmap.items():
        for val in vals:
            yield key, val

def product(numbers) :
    """Return the product of the numbers, eg: product([2, 3, 10]) == 60"""   
    result = 1
    for x in numbers:
        result *= x
    return result

def first(iterable, default = None):
    """Return the first element of an iterable, or default."""
    return next(iter(iterable), default)

def is_in(elt, seq):
    """Similar to (elt in seq), but compares with 'is', not '=='"""
    return any(x is elt for x in seq)

def mode(data):
    """Return the most common data item. If there are ties, return any one of them."""
    [(item, count)] = collections.Counter(data).most_common(1)
    return item 

def power_set(iterable):
    """power_set([1,2,3] --> (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    s = list(iterable)
    return list (chain.from_interable(combinations(s, r) for r in range(len(s) + 1))) [1:]

def extend(s, var, val):
    """Copy dict s and extend it by setting var to val; return copy."""
    return {**s, var: val}

def flatten(seqs):
    return sum(seqs, [])

# ______________________________________________________________________________
# argmin and argmax

identity = lambda x:x

def argmin_random_tie(seq, key = identity):
    """Return a minimum element of seq; break ties at random."""
    return min(shuffled(seq), key=key)

def argmax_random_tie(seq, key = identity):
    """Return an element with highest fn(seq[i] score; break ties at random)"""
    return max(shuffled(seq), key=key)

def shuffled(interable):
    """Randomly shuffle a copy of iterable."""
    items = list(interable)
    random.shuffle(items)
    return items

# ______________________________________________________________________________
# Statistical and mathematical functions

def histogram(values, mode = 0, bin_function = None):
    """Return a list of (value, count) pairs, summarizing the input values
    Sorted by increasing value, or if mode = 1, by decreasing count
    If bin_function is given, map it over value firsts"""
    if bin_function: 
        values = map(bin_function, values)

        bins = {}
        for val in values:
            bins[val] =  bins.get(val, 0) + 1

        if mode: 
            return sorted(list(bins.items()), key=lambda x: (x[1], x[0], reverse = True))
        else:
            return sorted(bins.items())

def dot_product(x, y):
    """Return the sum of the element-wise product of vectors x and y."""
    return sum(_x * _y for _x, _y in zip(x, y))

def element_wise_product(x, y):
    """Return the sum of the element-wise product of vectors x and y"""
    assert len(x) == len(y)
    return np.multiply(x, y)

def matrix_multiplication(x, *y):
    """Return a matrix as a matrix-multiplication of x and arbitrary number of matrices *y"""
    result = x
    for _y in y: 
        result = np.matmul(result, _y)
    return result 

def vector_add(a, b):
    """Component-wise addition of two vectors"""
    return tuple(map(operator.add, a, b))

def scalar_vector_product(x, y):
    """Return vector as a product of a scalar and a vector"""
    return np.multiply(x, y)

def probability(p):
    """Return true with probability p"""
    return p > random.uniform(0.0, 1.0)

def weighted_sample_with_replacement(n, seq, weights):
    """Pick n samples from seq at random, with replacement, with the probability 
    of each element in proportion to its corresponding
    weight"""
    sample = weighted_sampler(seq, weights)
    return [sample() for _ in range(n)]

def weighted_sampler(seq, weights):
    """Return a random-sample function that picks from seq weighted by erights"""
    totals = []
    for w in weights: 
        totals.append(w + totals[-1] if totals else w)
    return lambda: seq[bisect.bisect(totals, random.uniform(0, totals[-1]))]

def weighted_choice(choices):
    """A weighted version of random.choice"""
    total = sum(w for _, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r
            return c, w
        upto += w

def rounder(numbers, d=4):
    """Round a single number, or sequence of numbers, to d decimal places"""
    if isinstance(numbers, (int, float)):
        return round(numbers, d)
    else:
        constructor = type(numbers)
        return constructor(rounder(n, d) for n in numbers)
