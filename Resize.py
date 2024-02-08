import torchio as tio


# Function to resize an image
# source_path: absolute path to the image to resize
# output_path: absolute path to save the resized image
# output_size: tuple with the new size of the image (x, y, z)
def resize_image(source_path, output_path, output_size):
    # Load the image
    image = tio.ScalarImage(source_path)

    # Define the transformation (Resize) to resize the image
    transform = tio.Resize(output_size)

    # Apply the transformation to the image
    output = transform(image)

    # Save the transformed image to a new file
    output.save(output_path)
