import argparse
import multiprocessing
import shutil
from multiprocessing import Pool
from typing import Optional
import SimpleITK as sitk
from batchgenerators.utilities.file_and_folder_operations import *
from nnunetv2.paths import nnUNet_raw
from nnunetv2.dataset_conversion.generate_dataset_json import generate_dataset_json
from nnunetv2.utilities.dataset_name_id_conversion import find_candidate_datasets
from nnunetv2.configuration import default_num_processes
import numpy as np
import os


def split_3d_nifti(filename, output_folder):
    img_itk = sitk.ReadImage(filename)
    dim = img_itk.GetDimension()
    file_base = os.path.basename(filename)
    # num_training_cases =0
    if dim == 3:
        # print("yey: this is 3D")
        shutil.copy(filename, join(output_folder, file_base[:-7] + "_0000.nii.gz"))
        # JL Change
        shutil.copy(filename, join(output_folder, file_base[:-7] + ".nii.gz"))
        return
    else:
        raise RuntimeError("Unexpected dimensionality: %d of file %s, cannot split" % (dim, filename))


def convert_msd_dataset(source_folder: str, overwrite_target_id: Optional[int] = None,
                        num_processes: int = default_num_processes) -> None:
    if source_folder.endswith('/') or source_folder.endswith('\\'):
        source_folder = source_folder[:-1]

    #editted for MSK-yeshiva project to load n number of images
    train_num = 50 #change this num to increase/decrease the training images
    test_num = 10 #same here
    print(source_folder)

    labelsTr = join(source_folder, 'labelsTr')
    print(labelsTr)
    imagesTs = join(source_folder, 'imagesTs')
    imagesTr = join(source_folder, 'imagesTr')
    assert isdir(labelsTr), f"labelsTr subfolder missing in source folder"
    assert isdir(imagesTs), f"imagesTs subfolder missing in source folder"
    assert isdir(imagesTr), f"imagesTr subfolder missing in source folder"
    # dataset_json = join(source_folder, 'dataset.json')
    # assert isfile(dataset_json), f"dataset.json missing in source_folder"

    # infer source dataset id and name
    task, dataset_name = os.path.basename(source_folder).split('_')
    task_id = int(task[4:])

    # check if target dataset id is taken
    target_id = task_id if overwrite_target_id is None else overwrite_target_id
    existing_datasets = find_candidate_datasets(target_id)
    assert len(existing_datasets) == 0, f"Target dataset id {target_id} is already taken, please consider changing " \
                                        f"it using overwrite_target_id. Conflicting dataset: {existing_datasets} (check nnUNet_results, nnUNet_preprocessed and nnUNet_raw!)"

    target_dataset_name = f"Dataset{target_id:03d}_{dataset_name}"
    target_folder = join(nnUNet_raw, target_dataset_name)
    target_imagesTr = join(target_folder, 'imagesTr')
    target_imagesTs = join(target_folder, 'imagesTs')
    target_labelsTr = join(target_folder, 'labelsTr')
    print("Trying to make dir: " + target_imagesTr)
    maybe_mkdir_p(target_imagesTr)
    maybe_mkdir_p(target_imagesTs)
    maybe_mkdir_p(target_labelsTr)

    with multiprocessing.get_context("spawn").Pool(num_processes) as p:
        results = []

        source_images = [i for i in subfiles(imagesTr, suffix='.nii.gz', join=False) if
                         not i.startswith('.') and not i.startswith('_')]
        #limit the train images
        source_images = source_images[:train_num]
        source_images = [join(imagesTr, i) for i in source_images]

        results.append(
            p.starmap_async(
                split_3d_nifti, zip(source_images, [target_imagesTr] * len(source_images))
            )
        )

        source_images = [i for i in subfiles(imagesTs, suffix='.nii.gz', join=False) if
                         not i.startswith('.') and not i.startswith('_')]
        # limit the test images
        source_images = source_images[:test_num]
        source_images = [join(imagesTs, i) for i in source_images]

        results.append(
            p.starmap_async(
                split_3d_nifti, zip(source_images, [target_imagesTs] * len(source_images))
            )
        )

        # copy segmentations
        source_images = [i for i in subfiles(labelsTr, suffix='.nii.gz', join=False) if
                         not i.startswith('.') and not i.startswith('_')]
        # JL added line to limit the labels to the same number as the images
        source_images = source_images[:train_num]
        for s in source_images:
            shutil.copy(join(labelsTr, s), join(target_labelsTr, s))

        [i.get() for i in results]


    nifit_count = 0
    # print(target_imagesTr)
    training_path = target_imagesTr
    
    nifti_files = [file for file in os.listdir(training_path) if file.lower().endswith(".nii.gz")]
    nifti_count = len(nifti_files)
    print("This is how much training data",nifti_count)
    
    generate_dataset_json(
    str(target_folder),
    channel_names={
        0: "CT",
    },
    labels={
        "background": 0,
        "kidney": (1,2,3),
        "masses": (2,3),
        "tumor": 2,
    },
    regions_class_order=(1, 3, 2), #what is the class order
    file_ending=".nii.gz",
    num_training_cases=nifti_count,
    overwrite_image_reader_writer='NibabelIOWithReorient',
    )

    


def entry_point():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True,
                        help='Downloaded and extracted MSD dataset folder. CANNOT be nnUNetv1 dataset! Example: '
                             '/data/X/nnUNet_raw/Task07_Kidney')
    parser.add_argument('-overwrite_id', type=int, required=False, default=None,
                        help='Overwrite the dataset id. If not set we use the id of the MSD task (inferred from '
                             'folder name). Only use this if you already have an equivalently numbered dataset!')
    parser.add_argument('-np', type=int, required=False, default=default_num_processes,
                        help=f'Number of processes used. Default: {default_num_processes}')
    args = parser.parse_args()
    convert_msd_dataset(args.i, args.overwrite_id, args.np)


if __name__ == '__main__':
    print("Start converting kits data - 50 limit and ID is 295")
    convert_msd_dataset('/Users/judahlevy/data/X/nnUnet_Data/nnUNet_raw/Task07_Kidney/', overwrite_target_id=295)
    print("OK-Done!!")
