#!/usr/bin/env python3
__author__ = 'kowalski'
import itertools


def gen(*args, **kwargs):
    iters = list(args[0])
    num = []
    n = int(kwargs.popitem()[1])
    for j in range(n):
        for it in iters:
            num.append(it.__next__())
        num.sort()
        pop_num = num[0]
        i = 0
        while i < len(num) - 1:
            num[i] = num[i+1]
            i += 1
        del num[len(num)-1]
        yield pop_num


def test(*args,**kwargs):
    res = []
    for i in gen(list(args), n=kwargs.popitem()[1]):
        res.append(i)
    return res

print(test(itertools.count(1, 2), itertools.count(2, 3), n=10))
print(test(itertools.count(4, 3), itertools.count(1, 5),
           itertools.count(1, 5), n=10))
print(test(itertools.count(1, 5), itertools.count(2, 4),
           itertools.count(4, 3), itertools.count(5, 2), n=15))