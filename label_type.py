import cPickle as pickle
import cv2
import os
import numpy as np
import sys
import shutil
import glob
import random

def get_rotated_image(image,before_rotate_size,angle, pixels_to_jitter):
    center_x = before_rotate_size / 2 + (random.random() * pixels_to_jitter * 2) - pixels_to_jitter
    center_y = before_rotate_size / 2 + (random.random() * pixels_to_jitter * 2) - pixels_to_jitter
    rot_image = image.copy()
    m = cv2.getRotationMatrix2D((center_x, center_y), angle, 1)
    cv2.warpAffine(rot_image, m, (before_rotate_size, before_rotate_size), rot_image, cv2.INTER_CUBIC)
    # This is hard coded for 28x28.
    rot_image = cv2.resize(rot_image, (41, 41), interpolation=cv2.INTER_AREA)
    rot_image = rot_image[6:34, 6:34]
    return rot_image

def create_data_set(crop_dir,new_crop_dir,before_rotate_size,total_coins,crop):
    image_ids = []
    coins_ids = set()

    for root, dirnames, walk_filenames in os.walk(crop_dir):
        for filename in walk_filenames:
            if filename.endswith('.png'):
                image_id = int(filename.replace('.png', ''))
                image_ids.append([image_id, root , filename])
    print 'Total images in ' + crop_dir + ': ' + len(image_ids)

    image_ids = sorted(image_ids)

    for image_id, root, filename in image_ids:
        coin_id = image_id / 100
        coins_ids.add(coin_id)
        if len(coins_ids) <= total_coins:
            image = cv2.imread(root + '/' + filename)
            if image == None:
                print 'Is None: ' + filename
            else:
                if crop:
                    image = get_rotated_image(image, before_rotate_size, angle = 0, pixels_to_jitter = 0)
                else:
                    image = cv2.resize(image, (before_rotate_size, before_rotate_size), interpolation=cv2.INTER_AREA)
                cv2.imwrite(new_crop_dir + filename,image)


def create_design_data_set(labeled_designs,design_crop_dir,image_dir,test):
    labels = ['heads','tails']
    if test:
        pixels_to_jitter = 0
        angles = 1
    else:
        pixels_to_jitter = 2
        angles = 100

    for label in labels:
        dir = image_dir + label + '/'
        if not os.path.exists(dir):
            os.makedirs(dir)

    for coin_id, label in labeled_designs.iteritems():
        before_rotate_size = 56
        for image_id in range(0,56):
            #dir = design_crop_dir + str(coin_id / 100) + '/'
            class_dir = image_dir + label + '/'
            #for angle in range(0,10):
            filename = str(coin_id).zfill(5) + str(image_id).zfill(2) + '.png'
            image = cv2.imread(design_crop_dir + filename)
            image = cv2.resize(image, (before_rotate_size, before_rotate_size), interpolation=cv2.INTER_AREA)
            for count in range(0,angles):
                angle = random.random() * 360
                rot_image = get_rotated_image(image, before_rotate_size, angle, pixels_to_jitter)
                rotated_filename = filename.replace('.png', str(count).zfill(2) + '.png')
                cv2.imwrite(class_dir + rotated_filename,rot_image)
    sys.exit()

def label_heads_tails():
    cv2.namedWindow("next")
    coin_ids = []
    filenames = []
    images = {}
    labeled_designs = {}

    design_crop_dir = '/home/pkrush/data/cents-test/3/'
    image_dir = '/home/pkrush/cent-designs4/'
    test= False

    for filename in glob.iglob(design_crop_dir + '*54.png'):
        filenames.append([random.random(), filename])
        filenames.sort()
    print coin_ids

    for temp_random,filename in filenames:
        coin_id = filename.replace('54.png', '')
        coin_id = int(coin_id.replace(design_crop_dir, ''))
        coin_ids.append([coin_id,filename])

    for coin_id, filename in coin_ids:
        image = cv2.imread(filename)
        image = cv2.resize(image, (56,56),interpolation=cv2.INTER_AREA)
        #font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(image, str(coin_id % 100)[0:5], (4, 20), font, .7, (0, 255, 0), 2)
        images[coin_id] = image
        # while True:
        #     # display the image and wait for a keypress
        #     cv2.imshow("next", image)
        #     key = cv2.waitKey(1) & 0xFF
        #     if key == ord("n"):
        #         break
        #     if key == ord("q"):
        #         sys.exit()

    for count in range(0, len(coin_ids)):
        coin_id, filename = coin_ids[count]
        next = np.zeros((56, 560, 3), np.uint8)
        for count2 in range(0,10):
            if count + count2 >= len(coin_ids):
                continue
            next_coin_id = coin_ids[count + count2 ][0]
            if next_coin_id in images.iterkeys():
                next_image = images[next_coin_id]
            else:
                next_image = np.zeros((56, 56, 3), np.uint8)
            next[0:56,(9-count2) * 56:((10-count2) * 56)] = next_image

        while True:
            # display the image and wait for a keypress
            cv2.imshow("next", next)

            key = cv2.waitKey(1) & 0xFF
            if key !=255:
                print key

            if key == ord("h"):
                labeled_designs[coin_id] = 'heads'
                break
            if key == ord("t"):
                labeled_designs[coin_id] = 'tails'
                break
            if key == 27: #esc
                break

            if key == ord("q"):
                create_design_data_set(labeled_designs,design_crop_dir,image_dir,test)

    create_design_data_set(labeled_designs,design_crop_dir,image_dir,test)
    cv2.destroyAllWindows()

before_rotate_size = 56
crop_dir = '/home/pkrush/data/cents-test/'
new_crop_dir = '/home/pkrush/cents/'
crop_crop_dir = '/home/pkrush/cents-cropped/'


#total_coins is 1002 because 2 are missing images:
#create_data_set(crop_dir,new_crop_dir,before_rotate_size,total_coins=1002,crop=False)
#create_data_set(new_crop_dir,crop_crop_dir,before_rotate_size,total_coins=1000,crop=True)
#label_heads_tails()
