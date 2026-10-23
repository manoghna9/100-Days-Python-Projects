"""
Day 77 - NumPy Arrays

This file demonstrates:
- Creating ndarrays
- Dimensions
- Shape
- Data types
- Indexing
- Slicing
- Generating arrays
- Reshaping
- Broadcasting
- Scalar multiplication
- Matrix multiplication
"""

import numpy as np

#creating a 1D NumPy array

numbers = np.array([10, 20, 30, 40, 50])

print("1D NumPy array:")
print(numbers)

#checking type of the array
print("\nType:")
print(type(numbers))


# NumPy arrays have their own data type.
print("\nArray data type:")
print(numbers.dtype)


#array's dimensions

print("\nNumber of dimensions:")
print(numbers.ndim)

#array shape
print("\nShape:")
print(numbers.shape)


#numpy arrays can be multi-dimensional. Let's create a 2D array (matrix).

matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

print("\n2D array:")
print(matrix)

print("\nDimensions:")
print(matrix.ndim)

print("\nShape:")
print(matrix.shape)


#3d array (cube)

cube = np.array([
    [
        [1, 2],
        [3, 4]
    ],
    [
        [5, 6],
        [7, 8]
    ]
])

print("\n3D array:")
print(cube)

print("\nDimensions:")
print(cube.ndim)

print("\nShape:")
print(cube.shape)


#indexing a 1D array
print("\nFirst element:")
print(numbers[0])

print("\nThird element:")
print(numbers[2])

print("\nLast element:")
print(numbers[-1])


#indexing a 2D array (matrix)

print("\nMatrix:")
print(matrix)

# Row 0, column 1
print("\nElement at row 0, column 1:")
print(matrix[0, 1])

# Row 2, column 2
print("\nElement at row 2, column 2:")
print(matrix[2, 2])


#slicing a 1D array
print("\nFirst three elements:")
print(numbers[:3])

print("\nElements from index 2:")
print(numbers[2:])

print("\nEvery second element:")
print(numbers[::2])


#matrix slicing

print("\nFirst two rows:")
print(matrix[:2])

print("\nFirst two columns:")
print(matrix[:, :2])


#array range generation using np.arange()
sequence = np.arange(1, 11)

print("\nNumbers from 1 to 10:")
print(sequence)


# Start, stop, step
even_numbers = np.arange(
    2,
    21,
    2
)

print("\nEven numbers:")
print(even_numbers)

zeros = np.zeros(5)

print("\nArray of zeros:")
print(zeros)


# 2 rows × 3 columns
zero_matrix = np.zeros((2, 3))

print("\n2 x 3 zero matrix:")
print(zero_matrix)


#np.ones() creates an array filled with ones.
ones = np.ones(5)

print("\nArray of ones:")
print(ones)


one_matrix = np.ones((3, 3))

print("\n3 x 3 matrix of ones:")
print(one_matrix)

# 14. np.full() creates an array filled with a specified value.
filled = np.full(
    (2, 4),
    7
)

print("\n2 x 4 array filled with 7:")
print(filled)

#reshape 
numbers = np.arange(1, 13)

print("\nOriginal array:")
print(numbers)

reshaped = numbers.reshape(
    3,
    4
)

print("\nReshaped into 3 x 4:")
print(reshaped)

#array arithmetic operations
a = np.array([
    1,
    2,
    3
])

b = np.array([
    4,
    5,
    6
])

print("\na:")
print(a)

print("\nb:")
print(b)

print("\na + b:")
print(a + b)

print("\na - b:")
print(a - b)

print("\na * b:")
print(a * b)

print("\na / b:")
print(a / b)


#scalar multiplication
prices = np.array([
    100,
    200,
    300
])

print("\nOriginal prices:")
print(prices)

discounted_prices = prices * 0.9

print("\nPrices after 10% discount:")
print(discounted_prices)


#broadcasting

scores = np.array([
    [80, 85, 90],
    [70, 75, 80],
    [90, 95, 100]
])

bonus = 5

print("\nOriginal scores:")
print(scores)

print("\nScores after adding 5:")
print(scores + bonus)


# NumPy automatically applies the scalar
# to every element.


#broadcasting of arrays means that NumPy can perform operations on arrays of different shapes, 
#automatically expanding the smaller array to match the shape of the larger one.

marks = np.array([
    [70, 80, 90],
    [60, 70, 80]
])

extra_marks = np.array([
    5,
    10,
    15
])

print("\nOriginal marks:")
print(marks)

print("\nExtra marks:")
print(extra_marks)

print("\nAfter broadcasting:")
print(marks + extra_marks)


#matrix multiplication
matrix_a = np.array([
    [1, 2],
    [3, 4]
])

matrix_b = np.array([
    [5, 6],
    [7, 8]
])

print("\nMatrix A:")
print(matrix_a)

print("\nMatrix B:")
print(matrix_b)

print("\nElement-wise multiplication:")
print(matrix_a * matrix_b)

print("\nMatrix multiplication:")
print(matrix_a @ matrix_b)


# np.matmul() does the same thing.

print("\nUsing np.matmul():")
print(np.matmul(matrix_a, matrix_b))


#aggregate functions
data = np.array([
    [10, 20, 30],
    [40, 50, 60]
])

print("\nData:")
print(data)

print("\nTotal:")
print(data.sum())

print("\nMean:")
print(data.mean())

print("\nMaximum:")
print(data.max())

print("\nMinimum:")
print(data.min())


#axis argument specifies the dimension along which the operation is performed.
print("\nColumn totals:")
print(data.sum(axis=0))

print("\nRow totals:")
print(data.sum(axis=1))


print("\nDay 77 NumPy array experiments complete!")