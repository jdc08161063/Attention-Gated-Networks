import os
import subprocess
import SimpleITK as sitk

def mkdirfun(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def callmyfunction(mycmd):
    cmd = subprocess.Popen(mycmd, shell=True, executable="/bin/bash", stdout=subprocess.PIPE)
    stdoutput = cmd.communicate()[0].decode("utf-8") .strip('\n')
    print(stdoutput)
    return stdoutput

def exclude_images(input_list, query):
    new_list = []
    for name in input_list:
        if query not in name:
            new_list.append(name)
    return new_list

# Reverse axes
def reverse_image_direction(img_path, bool_dir=(False, False, False)):
    flipAboutOrigin = False
    img = sitk.ReadImage(img_path)
    flipped_img = sitk.Flip(img, bool_dir, flipAboutOrigin)
    sitk.WriteImage(flipped_img, img_path)

# Return Subdirs
def return_subdirs(path):
    output_list = sorted([os.path.join(path,name) for name in os.listdir(path) if os.path.isdir(os.path.join(path,name))])
    return output_list

# Find all files with extension
def find_files_ext(directory, extension):
    output_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                output_list.append(os.path.join(root,file))
    return output_list


# Source Image Directories
source_img_dir = '/vol/bitbucket/oo2113/TCIA/nifti_imgs'
source_lbl_dir = '/vol/bitbucket/oo2113/TCIA/nifti_lbls_c1'

# Target Image Directories
splits = ['train', 'validation']
n_folds = int(5)
source_images = sorted(find_files_ext(source_img_dir, '.nii.gz'))

# Generate KFold dataset
from sklearn.model_selection import KFold
kf = KFold(n_splits=n_folds, random_state=0, shuffle=True)
kf.get_n_splits(source_images)

for cv_index, (train_index, test_index) in enumerate(kf.split(source_images),1):
    print("TRAIN:", train_index, "TEST:", test_index)
    target_dir = '/vol/biomedic2/oo2113/dataset/tcia_dataset_cv_{0}'.format(str(cv_index)); mkdirfun(target_dir)
    source_dict = {'train': [source_images[j] for j in train_index],
                   'validation':  [source_images[j] for j in test_index]
                   }

    for split in splits:
        target_split_dir = os.path.join(target_dir, split); mkdirfun(target_split_dir)
        target_split_img_dir = os.path.join(target_split_dir, 'image'); mkdirfun(target_split_img_dir)
        target_split_lbl_dir = os.path.join(target_split_dir, 'label'); mkdirfun(target_split_lbl_dir)
        for source_image in source_dict[split]:
            img_basename = os.path.basename(source_image)
            source_label = os.path.join(source_lbl_dir, img_basename)
            os.symlink(source_image, os.path.join(target_split_img_dir, img_basename))
            os.symlink(source_label, os.path.join(target_split_lbl_dir, img_basename))
