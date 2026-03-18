import numpy as np

def standardize_rows(data,mean,std):
    """
    Subtracts the mean from each row of the data and divides by the standard deviation.
    Finally it returns return the resulting matrix. Does this 
    without using any numpy functions
    """
    return (data - mean) / std


def outer(x, y):
    """
    Autolab Write a Python function outer that receives two 
    vectors as input and returns the outer product of the two. 
    Do not use any NumPy functions. 
    
    Input: Two vectors as NumPy arrays of lenght and respectively. Output: The matrix giving the outer product.
    """
    return x[:,None] * y
    # her ændrer vi x fra shape (n,) til shape (n,1) ved at bruge none
    # altså gør vi den til en kolonnevektor
    # Nu ganger vi med entry y som har shape (m,) og numpy vil 
    # # automatisk udvide y til shape (1,m) så vi får en matrix med 
    # shape (n,m) som er det ønskede output.


def distmat_1d(x,y):
    return abs(x[:,None] - y)