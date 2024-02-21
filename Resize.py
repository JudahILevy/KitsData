# # import torchio as tio

# # # Function to resize an image
# # # source_path: absolute path to the image to resize
# # # output_path: absolute path to save the resized image
# # # output_size: tuple with the new size of the image (x, y, z)

# # def resize_image(source_path, output_path, output_size):
# #     # Load the image
# #     image = tio.ScalarImage(source_path)

# #     # Get the original z-axis value
# #     original_z = image.spatial_shape[2]

# #     # Modify the output_size tuple to keep the original z-axis value
# #     output_size = (output_size[0], output_size[1], original_z)

# #     # Define the transformation (Resize) to resize the image
# #     transform = tio.Resize(output_size)

# #     # Apply the transformation to the image
# #     output = transform(image)

# #     # Save the transformed image to a new file
# #     output.save(output_path)


# import ants
# import os

# def resize_image(source_path, output_path, output_size):
#     # Load the image
#     image = ants.image_read(source_path)

#     # Define the new size (x, y, z)
#     new_size = (output_size[0], output_size[1], image.shape[-1])

#     # Resample the image
#     resized_image = ants.resample_image(image, new_size)

#     # Save the resized image
#     ants.image_write(resized_image, output_path)

# # if __name__ == "__main__":
# #     # Example usage
# #     source_image_path = "imaging.nii.gz"
# #     output_image_path = "kidney_resampled.nii.gz"
# #     target_size = (128, 128)  # Adjust as needed

# #     resize_image(source_image_path, output_image_path, target_size)
import torchio as tio

# Function to resize an image
# source_path: absolute path to the image to resize
# output_path: absolute path to save the resized image
# output_size: tuple with the new size of the image (x, y, z)
def resize_image(source_path, output_path, output_size):
    # Load the image
    image = tio.ScalarImage(source_path)

    # Get the original z-axis value
    original_z = image.spatial_shape[2]

    # Modify the output_size tuple to keep the original z-axis value
    output_size = (output_size[0], output_size[1], original_z)

    # Define the transformation (Resize) to resize the image
    transform = tio.Resize(output_size)

    # Apply the transformation to the image
    output = transform(image)

    # Save the transformed image to a new file
    output.save(output_path)

