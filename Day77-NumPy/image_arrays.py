"""
Day 77 - Images as NumPy Arrays

An image can be represented as a NumPy ndarray.

For an RGB image:

    height x width x 3

The final dimension contains:
    [Red, Green, Blue]
"""

from pathlib import Path

import numpy as np
from PIL import Image


IMAGE_FOLDER = Path("images")

INPUT_IMAGE = IMAGE_FOLDER / "sample.jpg"
OUTPUT_IMAGE = IMAGE_FOLDER / "modified_sample.png"


# ============================================================
# 1. LOAD IMAGE
# ============================================================

image = Image.open(INPUT_IMAGE)

print("Image loaded successfully.")

print("\nImage size:")
print(image.size)

print("\nImage mode:")
print(image.mode)


# ============================================================
# 2. CONVERT IMAGE TO NUMPY ARRAY
# ============================================================

image_array = np.array(image)

print("\nNumPy array:")
print(image_array)


# ============================================================
# 3. ARRAY INFORMATION
# ============================================================

print("\nArray type:")
print(type(image_array))

print("\nArray shape:")
print(image_array.shape)

print("\nNumber of dimensions:")
print(image_array.ndim)

print("\nData type:")
print(image_array.dtype)


# ============================================================
# 4. ACCESS A PIXEL
# ============================================================

pixel = image_array[0, 0]

print("\nTop-left pixel:")
print(pixel)


# ============================================================
# 5. ACCESS RGB CHANNELS
# ============================================================

red = image_array[:, :, 0]

green = image_array[:, :, 1]

blue = image_array[:, :, 2]

print("\nRed channel shape:")
print(red.shape)

print("\nGreen channel shape:")
print(green.shape)

print("\nBlue channel shape:")
print(blue.shape)


# ============================================================
# 6. CREATE A RED-TINTED IMAGE
# ============================================================

red_image = image_array.copy()

# Remove green.
red_image[:, :, 1] = 0

# Remove blue.
red_image[:, :, 2] = 0


red_result = Image.fromarray(red_image)

red_output = (
    IMAGE_FOLDER /
    "red_tinted.png"
)

red_result.save(red_output)

print(
    f"\nRed-tinted image saved to {red_output}"
)


# ============================================================
# 7. CREATE A GREEN-TINTED IMAGE
# ============================================================

green_image = image_array.copy()

green_image[:, :, 0] = 0
green_image[:, :, 2] = 0

green_result = Image.fromarray(
    green_image
)

green_output = (
    IMAGE_FOLDER /
    "green_tinted.png"
)

green_result.save(
    green_output
)

print(
    f"Green-tinted image saved to {green_output}"
)


# ============================================================
# 8. CREATE A BLUE-TINTED IMAGE
# ============================================================

blue_image = image_array.copy()

blue_image[:, :, 0] = 0
blue_image[:, :, 1] = 0

blue_result = Image.fromarray(
    blue_image
)

blue_output = (
    IMAGE_FOLDER /
    "blue_tinted.png"
)

blue_result.save(
    blue_output
)

print(
    f"Blue-tinted image saved to {blue_output}"
)


# ============================================================
# 9. MODIFY A REGION
# ============================================================

region_image = image_array.copy()

height, width, channels = region_image.shape

# Paint a small rectangle black.
region_image[
    :height // 4,
    :width // 4
] = 0


region_result = Image.fromarray(
    region_image
)

region_output = (
    IMAGE_FOLDER /
    "modified_region.png"
)

region_result.save(
    region_output
)

print(
    f"\nModified region saved to {region_output}"
)


print("\nImage manipulation complete!")