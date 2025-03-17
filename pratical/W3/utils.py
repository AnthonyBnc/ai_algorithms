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

