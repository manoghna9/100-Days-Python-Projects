"""
Day 77 - Advanced NumPy

Main demonstration file.

This project demonstrates the fundamental NumPy concepts
introduced in Day 77 of the course.
"""

import numpy as np


# ============================================================
# 1. CREATE ARRAYS
# ============================================================

print("=" * 60)
print("DAY 77 - NUMPY")
print("=" * 60)


numbers = np.array([
    10,
    20,
    30,
    40,
    50
])

print("\n1. Basic ndarray:")
print(numbers)


# ============================================================
# 2. ARRAY PROPERTIES
# ============================================================

print("\n2. Array properties")

print("Type:")
print(type(numbers))

print("Dimensions:")
print(numbers.ndim)

print("Shape:")
print(numbers.shape)

print("Data type:")
print(numbers.dtype)


# ============================================================
# 3. TWO-DIMENSIONAL ARRAY
# ============================================================

matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

print("\n3. Matrix:")
print(matrix)

print("\nMatrix shape:")
print(matrix.shape)


# ============================================================
# 4. INDEXING
# ============================================================

print("\n4. Indexing")

print("First element:")
print(numbers[0])

print("Last element:")
print(numbers[-1])

print("Matrix [0, 1]:")
print(matrix[0, 1])


# ============================================================
# 5. SLICING
# ============================================================

print("\n5. Slicing")

print("First three:")
print(numbers[:3])

print("Last three:")
print(numbers[-3:])

print("Every second element:")
print(numbers[::2])


# ============================================================
# 6. GENERATING ARRAYS
# ============================================================

print("\n6. Generating arrays")

print("arange:")
print(np.arange(1, 11))

print("\nzeros:")
print(np.zeros(5))

print("\nones:")
print(np.ones(5))

print("\nfull:")
print(np.full(5, 7))


# ============================================================
# 7. RESHAPING
# ============================================================

sequence = np.arange(1, 13)

matrix_3x4 = sequence.reshape(
    3,
    4
)

print("\n7. Reshaping")

print("Original:")
print(sequence)

print("\n3 x 4:")
print(matrix_3x4)


# ============================================================
# 8. ELEMENT-WISE OPERATIONS
# ============================================================

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

print("\n8. Element-wise operations")

print("Addition:")
print(a + b)

print("Subtraction:")
print(a - b)

print("Multiplication:")
print(a * b)

print("Division:")
print(a / b)


# ============================================================
# 9. BROADCASTING
# ============================================================

scores = np.array([
    [80, 85, 90],
    [70, 75, 80],
    [90, 95, 100]
])

print("\n9. Broadcasting")

print("Original scores:")
print(scores)

print("\nAdd 5 to every value:")
print(scores + 5)


# ============================================================
# 10. ARRAY BROADCASTING
# ============================================================

bonus = np.array([
    5,
    10,
    15
])

print("\nBonus:")
print(bonus)

print("\nBroadcasted result:")
print(scores + bonus)


# ============================================================
# 11. MATRIX MULTIPLICATION
# ============================================================

A = np.array([
    [1, 2],
    [3, 4]
])

B = np.array([
    [5, 6],
    [7, 8]
])

print("\n10. Matrix multiplication")

print("A:")
print(A)

print("\nB:")
print(B)

print("\nElement-wise multiplication:")
print(A * B)

print("\nMatrix multiplication:")
print(A @ B)


# ============================================================
# 12. AGGREGATION
# ============================================================

data = np.array([
    [10, 20, 30],
    [40, 50, 60]
])

print("\n11. Aggregation")

print("Sum:")
print(data.sum())

print("Mean:")
print(data.mean())

print("Maximum:")
print(data.max())

print("Minimum:")
print(data.min())

print("\nColumn totals:")
print(data.sum(axis=0))

print("\nRow totals:")
print(data.sum(axis=1))


# ============================================================
# 13. BOOLEAN FILTERING
# ============================================================

values = np.array([
    5,
    12,
    18,
    3,
    25,
    9
])

print("\n12. Boolean filtering")

large_values = values[
    values > 10
]

print("Values greater than 10:")
print(large_values)


# ============================================================
# 14. A SMALL REAL-WORLD EXAMPLE
# ============================================================

temperatures = np.array([
    24,
    26,
    28,
    31,
    30,
    27,
    25
])

print("\n13. Weekly temperature example")

print("Temperatures:")
print(temperatures)

print(
    "Average temperature:",
    temperatures.mean()
)

print(
    "Highest temperature:",
    temperatures.max()
)

print(
    "Lowest temperature:",
    temperatures.min()
)

print(
    "Days above 27 degrees:",
    np.sum(temperatures > 27)
)


# ============================================================
# FINISHED
# ============================================================

print("\n" + "=" * 60)
print("DAY 77 NUMPY DEMONSTRATION COMPLETE")
print("=" * 60)