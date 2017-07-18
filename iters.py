#!/usr/bin/env python

def iter_block(check,r):
    """
    Iterates through 'r', yielding a block in list form of items in r since the
    prior True result tested against the 'check' function.
    """
    bunch = []
    try:
        tr = iter(r)
        bunch.append(next(tr))
        while True:
            a = next(tr)
            if check(a):
                yield bunch
                bunch = []
            bunch.append(a)
    except StopIteration:
        if len(bunch) > 0:
            yield bunch

def iter_block_end(check,r):
    """
    Same as iter_block, except check's True occurs at the close of a block.
    """
    bunch = []
    try:
        tr = iter(r)
        while True:
            a = next(tr)
            bunch.append(a)
            if check(a):
                yield bunch
                bunch = []
    except StopIteration:
        if len(bunch) > 0:
            yield bunch


