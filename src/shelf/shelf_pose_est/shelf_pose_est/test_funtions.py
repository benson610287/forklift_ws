import numpy as np


# # Example 3D array
# arr = np.random.rand(4, 4, 2)
# print("random")
# print(arr)

# first_x_values = arr[:, 0, 0]  # Shape: (4,) - first x-coord of each object
# sort_indices = np.argsort(first_x_values)
# sorted_arr = arr[sort_indices]
# print("sort x")
# print(sorted_arr)

# first_half = sorted_arr[:2]
# second_half = sorted_arr[2:]
# # Sort by first point's y-coordinate of each object
# first_y_values = first_half[:, 0, 1]  # Shape: (4,) - first y-coord of each object
# sort_indices = np.argsort(first_y_values)
# print("sorted indices: ",sort_indices)
# sorted_first_half = first_half[sort_indices]

# first_y_values = second_half[:, 0, 1]  # Shape: (4,) - first y-coord of each object
# sort_indices = np.argsort(first_y_values)
# sorted_second_half = second_half[sort_indices]

# sorted_arr = np.concatenate([sorted_first_half, sorted_second_half], axis=0)
# print("sort y")
# print(sorted_arr)

# array = np.random.rand(4, 2)
array = np.array([[1,2],[3,4],[5,6],[7,8]])
print(array)
topmid = (array[0] + array[1]) / 2
print(topmid)
