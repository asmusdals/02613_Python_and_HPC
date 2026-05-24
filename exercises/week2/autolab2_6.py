import sys 

numbers = [int(x) for x in sys.argv[1:]]

even_numbers = list(filter(lambda x: x % 2 == 0, numbers))

print(even_numbers)