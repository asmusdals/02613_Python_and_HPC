import sys

def listsum(a):
    sum = 0
    for i in range(len(a)):
        sum += a[i]
    return sum


def deduplicate(arr):
    seen = set()
    result = []
    for item in arr:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def sorttuples(arr):
    return sorted(arr, key=lambda x: x[1])

def squarecubes(arr):
    squares = [x**2 for x in arr]
    cubes = [x**3 for x in arr]
    return (squares, cubes)


a = [1,2,3]
print(listsum(a))
print(deduplicate([1,2,3,4,5,1,2,3]))
print(sorttuples([(1, 3), (2, 2), (3, 1)]))
print(squarecubes([1,2,3,4]))