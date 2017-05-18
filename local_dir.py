import os
data = '/home/pkrush/lighting-augmentation-data/'
small_crop = data + 'cents/'
crop_crop = data + 'cents-cropped/'
labeled_crop = data + 'cents-labeled/'

def make_local_dir():
    directories = [data, small_crop, crop_crop, labeled_crop]
    for path_name in directories:
        if not os.path.exists(path_name):
            os.makedirs(path_name)