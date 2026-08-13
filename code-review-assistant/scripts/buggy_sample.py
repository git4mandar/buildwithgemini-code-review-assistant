# buggy_sample.py
import os
import sys

# Issue 1: Global variable used and modified poorly
x = 10

def add_to_x(num):
    # Issue 2: Using global keyword without a good reason
    global x
    x = x + num
    return x

# Issue 3: Mutable default argument
def append_to_list(val, my_list=[]):
    my_list.append(val)
    return my_list

# Issue 4: Security risk - using eval() on raw input
def calculate_expression(expr):
    return eval(expr)

# Issue 5: Bare except clause and poor error handling
def divide_numbers(a, b):
    try:
        return a / b
    except:
        print("An error occurred!")
        # Issue 6: Returning None implicitly on error, causing downstream issues
        

# Issue 7: Unused import and unused variable
def unused_example():
    unused_var = 42
    print("Hello, world!")

if __name__ == "__main__":
    print(add_to_x(5))
    print(append_to_list(1))
    print(append_to_list(2))  # Will unexpectedly contain [1, 2]
    divide_numbers(10, 0)