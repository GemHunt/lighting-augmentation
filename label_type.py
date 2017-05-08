import cPickle as pickle
import cv2
import os
import numpy as np
import sys
import shutil
import glob
import random

data_dir = '/home/pkrush/cent-date-models/metadata/'
crop_dir = '/home/pkrush/cent-dates/'
classify_dir = '/home/pkrush/cent-dates-classify/'

def get_filename(coin_id):
    dir = crop_dir + str(coin_id / 100) + '/'
    return dir + str(coin_id).zfill(5) + str(54).zfill(2) + '.png'

def copy_images_for_classification():
    ground_truth_dates = pickle.load(open(data_dir + 'ground_truth_dates.pickle', "rb"))
    ground_truth_dates = sorted(ground_truth_dates, key=lambda x: x[3], reverse=False)
    if not os.path.exists(classify_dir):
        os.mkdir(classify_dir)

    for seed_id, coin_id, result, labeled_date, bad_angle, bad_image in ground_truth_dates:
        if labeled_date < 1900:
            continue
        dir = crop_dir + str(coin_id / 100) + '/'
        new_dir = classify_dir + str(labeled_date) + '/'
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        for image_id in range(0,57):
            filename = str(coin_id).zfill(5) + str(image_id).zfill(2) + '.png'
            old_filename = dir + filename
            new_filename = new_dir + filename
            shutil.copyfile(old_filename,new_filename)


def save_and_exit(labeled_dates,ground_truth_dates):
    #pickle.dump(labeled_dates, open(data_dir + 'labeled_dates.pickle', "wb"))
    new_ground_truth_dates = []
    for seed_id, coin_id, result, labeled_date, bad_angle, bad_image in ground_truth_dates:
       if coin_id in labeled_dates.iterkeys():
           labeled_date = labeled_dates[coin_id]
       new_ground_truth_dates.append([seed_id, coin_id, result, labeled_date, bad_angle, bad_image])

    pickle.dump(new_ground_truth_dates, open(data_dir + 'ground_truth_dates.pickle', "wb"))
    sys.exit()


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
                center_x = before_rotate_size / 2 + (random.random() * pixels_to_jitter * 2) - pixels_to_jitter
                center_y = before_rotate_size / 2 + (random.random() * pixels_to_jitter * 2) - pixels_to_jitter
                rot_image = image.copy()
                m = cv2.getRotationMatrix2D((center_x, center_y), angle, 1)
                cv2.warpAffine(rot_image, m, (before_rotate_size, before_rotate_size), rot_image, cv2.INTER_CUBIC)
                # This is hard coded for 28x28.
                rot_image = cv2.resize(rot_image, (41, 41), interpolation=cv2.INTER_AREA)
                rot_image = rot_image[6:34, 6:34]
                rotated_filename = filename.replace('.png', str(count).zfill(2) + '.png')
                cv2.imwrite(class_dir + rotated_filename,rot_image)
    sys.exit()

def label_date():
    cv2.namedWindow("next")

    ground_truth_dates = pickle.load(open(data_dir + 'ground_truth_dates.pickle', "rb"))
    #labeled_dates = pickle.load(open(data_dir + 'labeled_dates.pickle', "rb"))
    labeled_dates = {}
    ground_truth_date_dict = {}

    images = {}

    ground_truth_dates = sorted(ground_truth_dates, key=lambda x: x[3], reverse=False)

    for count in range(0,len(ground_truth_dates)):
        seed_id,coin_id, result,labeled_date,bad_angle,bad_image = ground_truth_dates[count]
        if coin_id in labeled_dates.iterkeys():
            pass
            #continue
        filename = get_filename(coin_id)
        if not os.path.exists(filename):
            labeled_dates[coin_id] = -2
            continue
        image = cv2.imread(filename)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, str(labeled_date % 100)[0:5], (4, 20), font, .7, (0, 255, 0), 2)

        images[coin_id] = image

        last_labeled_date = 0

    for count in range(0, len(ground_truth_dates)):
        seed_id, coin_id, result, old_labeled_date, bad_angle, bad_image = ground_truth_dates[count]
        if not coin_id in images.iterkeys():
            continue
        next = np.zeros((56, 560, 3), np.uint8)
        for count2 in range(0,10):
            if count + count2 >= len(ground_truth_dates):
                continue
            next_coin_id = ground_truth_dates[count + count2 ][1]
            if next_coin_id in images.iterkeys():
                next_image = images[next_coin_id]
            else:
                next_image = np.zeros((56, 56, 3), np.uint8)
            next[0:56,(9-count2) * 56:((10-count2) * 56)] = next_image

        decade  = -1
        year = -1
        labeled_date = -999

        while True:
            # display the image and wait for a keypress
            cv2.imshow("image", images[coin_id])
            cv2.imshow("next", next)

            key = cv2.waitKey(1) & 0xFF
            if key !=255:
                print key

            if key == ord("a"):
                labeled_date = 0
            if key == ord("b"):
                labeled_date = -1


            if 47 < key < 58:
                if decade == -1:
                    decade = key - 48
                else:
                    year = key - 48
                    if decade < 2:
                        labeled_date = 2000 + decade * 10 + year
                    else:
                        labeled_date  = 1900 + decade * 10 + year

            if key == 10: #enter
                labeled_date = last_labeled_date

            if labeled_date != -999:
                 labeled_dates[coin_id] = labeled_date
                 print labeled_date
                 last_labeled_date = labeled_date
                 break

            if key == 27: #esc
                break

            if key == ord("q"):
                save_and_exit(labeled_dates,ground_truth_dates)

    save_and_exit(labeled_dates,ground_truth_dates)
    cv2.destroyAllWindows()


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



label_heads_tails()
#copy_images_for_classification()
