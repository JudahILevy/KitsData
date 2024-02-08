import os
import shutil

from Resize import resize_image

output_size = (128, 128, 128)
# note: in our data, z always seems to be at a max of 128 already

def main(dataset_folder,nnRaw_folder):
    # dataset_folder = input("Enter the absolute path to the dataset folder: ")
    
    # Replace 'path_to_your_dataset_folder' with the actual path to your dataset folder
    
    destination_directory = nnRaw_folder+'/Task07_Kidney/'
    
    # Create destination_directory if it does not exist
    os.makedirs(destination_directory, exist_ok=True)
    
    # Create new folders if they don't exist
    images_tr_folder = os.path.join(destination_directory, 'imagesTr')
    images_ts_folder = os.path.join(destination_directory, 'imagesTs')
    labels_tr_folder = os.path.join(destination_directory, 'labelsTr')
    labels_ts_folder = os.path.join(destination_directory, 'labelsTs')

    os.makedirs(images_tr_folder, exist_ok=True)
    os.makedirs(labels_tr_folder, exist_ok=True)
    os.makedirs(labels_ts_folder, exist_ok=True)
    os.makedirs(images_ts_folder, exist_ok=True)
        
    # Iterate through each case folder in the dataset
    for case_folder in os.listdir(dataset_folder):
        if not case_folder.startswith('case_'):
            continue
        print(case_folder)
        case_folder_path = os.path.join(dataset_folder, case_folder)
    
        # Check if it is a directory
        if os.path.isdir(case_folder_path):
            # Extract the numeric part from the case folder name
            # numeric_part = ''.join(filter(str.isdigit, case_folder))
            numeric_part = case_folder[6:]
    
            # Construct the new filenames
            imaging_filename = f'kidney_{numeric_part}.nii.gz'
            segmentation_filename = f'kidney_{numeric_part}.nii.gz'
    
            # Source paths
            imaging_source_path = os.path.join(case_folder_path, 'imaging.nii.gz')
            segmentation_source_path = os.path.join(case_folder_path, 'segmentation.nii.gz')
    
            # Destination paths
            imaging_dest_path = os.path.join(images_tr_folder, imaging_filename)
            segmentation_dest_path = os.path.join(labels_tr_folder, segmentation_filename)
    
            # Rename and move the files
            shutil.move(imaging_source_path, imaging_dest_path)
            shutil.move(segmentation_source_path, segmentation_dest_path)

            # Resize the images after moving them
            resize_image(imaging_dest_path, imaging_dest_path, output_size)
            resize_image(segmentation_dest_path, segmentation_dest_path, output_size)
    
    print("Conversion completed successfully.")
