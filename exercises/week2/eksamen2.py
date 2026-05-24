
def listsum(a):
    sum = 0
    for i in a:
        sum += i
    return sum


def deduplicate(arr):
    seen = set()
    result = []
    for item in arr:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def squarecubes(arr):
    square = [x**2 for x in arr]
    cube = [x**3 for x in arr]
    return (square,cube)


a = [1,2,3,4]    
print(listsum(a))
print(deduplicate(a))
print(squarecubes(a))