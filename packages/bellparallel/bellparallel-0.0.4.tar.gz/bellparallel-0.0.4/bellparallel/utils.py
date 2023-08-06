"""
Utils package for data processing
"""

def lsum(elems):
    out = []
    for elem in elems:
        out.extend(elem)
    return out

def peek(elem):
    print(elem)
    return elem

def lmap(func, elems):
    return list(map(func, elems))
