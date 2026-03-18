import sys

grades = [float(x) for x in sys.argv[1:]]

mean = sum(grades) / len(grades)

result = "Pass" if mean >= 5.0 else "Fail"

print(f"{mean} {result}")


