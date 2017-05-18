import numpy as np
import os
import sys
import cv2
import local_dir as dir
import time

sys.path.append('/home/pkrush/caffe/python')
import caffe

def get_classifier(model_name, crop_size):
    model_dir = model_name + '/'
    MODEL_FILE = model_dir + 'deploy.prototxt'
    PRETRAINED = model_dir + 'snapshot.caffemodel'
    meanFile = model_dir + 'mean.binaryproto'

    # Open mean.binaryproto file
    blob = caffe.proto.caffe_pb2.BlobProto()
    data = open(meanFile, 'rb').read()
    blob.ParseFromString(data)
    mean_arr = np.array(caffe.io.blobproto_to_array(blob)).reshape(1, crop_size, crop_size)
    print mean_arr.shape

    net = caffe.Classifier(MODEL_FILE, PRETRAINED, image_dims=(crop_size, crop_size), mean=mean_arr, raw_scale=255)
    return net

def get_labels(model_name):
    labels_file = model_name + '/labels.txt'
    labels = [line.rstrip('\n') for line in open(labels_file)]
    return labels

def make_dir(directories):
    for path_name in directories:
        if not os.path.exists(path_name):
            os.makedirs(path_name)

def get_caffe_image(crop, crop_size):
    # this is how you get the image from file:
    # coinImage = [caffe.io.load_image("some file", color=False)]

    caffe_image = cv2.resize(crop, (crop_size, crop_size), interpolation=cv2.INTER_AREA)
    caffe_image = caffe_image.astype(np.float32) / 255
    caffe_image = np.array(caffe_image).reshape(crop_size, crop_size, 1)
    # Caffe wants a list so []:
    return [caffe_image]


def get_composite_image(images, rows, cols):
    crop_rows, crop_cols, channels = images[0].shape
    composite_rows = crop_rows * rows
    composite_cols = crop_cols * cols
    composite_image = np.zeros((composite_rows, composite_cols, 3), np.uint8)
    key = 0
    for x in range(0, rows):
        for y in range(0, cols):
            key += 1
            if len(images) <= key:
                break
            if images[key] is not None:
                composite_image[x * crop_rows:((x + 1) * crop_rows), y * crop_cols:((y + 1) * crop_cols)] = images[key]
    return composite_image

start_time = time.time()
crop_size = 28
heads_tails = get_classifier("heads_tails_model", crop_size)
heads_tails_labels = get_labels('heads_tails_model')
count = 0

image_ids = []

for root, dirnames, walk_filenames in os.walk(dir.crop_crop):
    for filename in walk_filenames:
        if filename.endswith('.png'):
            image_id = int(filename.replace('.png', ''))
            image_ids.append([image_id, root, filename])

image_ids = sorted(image_ids)
coin_scores = {}
thumbnails = {}

for image_id, root, filename in image_ids:
    coin_id = image_id / 100
    crop = cv2.imread(root + '/' + filename)
    if crop is None:
        continue
    if image_id % 100 == 54:
        thumbnail_filename = dir.small_crop + filename
        thumbnail = cv2.imread(thumbnail_filename)
        if thumbnail is not None:
            thumbnails[coin_id] = thumbnail
    crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    score = heads_tails.predict(get_caffe_image(crop, crop_size), oversample=False)
    if coin_id in coin_scores.iterkeys():
        coin_scores[coin_id] = coin_scores[coin_id] + score
    else:
        coin_scores[coin_id] = score

    coin_type = heads_tails_labels[np.argmax(score)]
    max_value = np.amax(score)

    print image_id, coin_type, score, max_value

results = []

for coin_id, score in coin_scores.iteritems():
    coin_type = heads_tails_labels[np.argmax(score)]
    # There are 57 images and 100/57 is needed to take it to 100%
    max_value = np.amax(score) * 100 / 57
    results.append([coin_id, coin_type, max_value])

results = sorted(results, key=lambda result: result[2], reverse=True)
results = sorted(results, key=lambda result: result[1], reverse=True)
images = []

for coin_id, coin_type, max_value in results:
    if coin_id not in thumbnails.iterkeys():
        print coin_id, 'coin_id not in thumbnails.iterkeys():'
        continue
    crop = thumbnails[coin_id]
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(crop, str(int(max_value)), (4, 15), font, .5, (0, 200, 0), 2)
    # cv2.putText(crop, str(coin_id), (4, 40), font, .4, (0, 255, 0), 2)
    images.append(crop)

composite = get_composite_image(images, 50, 20)
# cv2.namedWindow("results")
cv2.imwrite(dir.labeled_crop + 'results.png', composite)

# while True:
#     cv2.imshow("results",composite)
#     key = cv2.waitKey(1) & 0xFFshutil
#     if key == ord("q"):
#         break
print 'Done in %s seconds' % (time.time() - start_time,)
cv2.destroyAllWindows()
