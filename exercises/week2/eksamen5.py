import sys 

grades = [float(x) for x in sys.argv[1:]]

num_grades = len(grades)
sum_grades = sum(grades)
mean_grade = sum_grades / num_grades

if mean_grade >= 5:
    pass_fail_bool = "pass"
else:
    pass_fail_bool = "failed"
    
print(f"{mean_grade} you {pass_fail_bool}")