import lzma
import json
import os
import pandas as pd 
import shutil
import glob
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

with open('../config.json') as f:
  config = json.load(f)

EXCLUDE_FACES = False

if not EXCLUDE_FACES:
    KEY = config['face']['KEY']
    ENDPOINT = config['face']['ENDPOINT']
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def count_faces(image_url):
    test_image_array = glob.glob(url)
    image = open(test_image_array[0], 'r+b')
    faces = face_client.face.detect_with_stream(image, detection_model='detection_02')
    return len(faces)

def get_likes(path):
    data = lzma.open(path).read()
    data = json.loads(data)
    return data['node']["edge_liked_by"]['count']


folders = config['hashtags']
image_data = []

for folder in folders:
    files = [folder+'/'+f for f in os.listdir(folder) if f.endswith('.xz')]
    image_files = [folder+'/'+f for f in os.listdir(folder) if f.endswith('.jpg')]

    for f in files:

        path = f.replace('.json.xz','')
        image = [i for i in image_files if i.startswith(path)]

        for i in image:

            if not EXCLUDE_FACES:
                if count_faces(i) == 0:
                    continue

            image_data.append({
                'image': i,
                'likes': get_likes(f)
            })

bucket_count = 5

image_data = pd.DataFrame(image_data)
image_data['buckets'] = pd.qcut(image_data['likes'],q=bucket_count,precision=0,labels=False)

print(image_data['buckets'].value_counts())

if not os.path.exists('data'):
    os.makedirs('data')

bucket_map = {}
for i in range(bucket_count):
    bucket_map[i] = []

for index, row in image_data.iterrows():
    bucket_map[row['buckets']].append(row['image'])
    
for index in range(bucket_count):
    path = 'data/'+str(index)
    if not os.path.exists(path):
        os.makedirs(path)

    for i in range(len(bucket_map[index])):
        location = i//95
        final_path = path+'/'+str(location)
        if not os.path.exists(final_path):
            os.makedirs(final_path)
        shutil.copy(bucket_map[index][i], final_path)

print('Total Images: ', image_data.shape[0])