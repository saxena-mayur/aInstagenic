import streamlit as st
import io
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import json

with open('config.json') as f:
  config = json.load(f)

ENDPOINT = config['vision']['ENDPOINT']
prediction_key = config['vision']['prediction_key']
project_id= config['vision']['project_id']
publish_iteration_name = config['vision']['publish_iteration_name']

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

def convert_PIL_to_byte(image):
    image = image.convert('RGB')
    buf = io.BytesIO()
    image.save(buf, format='JPEG')
    content = buf.getvalue()
    return content

def design_output(score):
    response = ""
    for i in range(score+1):
        response+= str(":heart:")
    for i in range(4-score):
        response+= str(":broken_heart:")
    return response

def predict_image_class(image):
    results = predictor.classify_image(project_id, publish_iteration_name, convert_PIL_to_byte(image))
    output = {}
    for prediction in results.predictions:
        output[prediction.tag_name] = prediction.probability * 100
    
    max_key = max(output, key=output.get)
    return int(max_key)

title = 'aInstagenic'
st.set_page_config(page_title=title, page_icon=":camera:", layout="wide", initial_sidebar_state='auto')
st.title(':camera: '+title)
st.subheader('On Instagram, there’s no room for “good enough” shots. Time to level up using AI.')
for i in range(2):
    st.text('\n')

file_up = st.file_uploader("Upload an image", type=["jpg","png","jpeg"])

col1, col2 = st.beta_columns(2)

if file_up is not None:
    from PIL import Image
    image = Image.open(file_up)
    col1.image(image, caption='Uploaded Image.', use_column_width=True)
    col2.header('Rating: ')
    col2.header(design_output(predict_image_class(image)))

    for i in range(10):
        col2.text(" \n")
    col2.write('Note:')
    col2.write(':arrow_right: If the AI thinks that this photograph will get more likes on Instagram, it will give it more :heart:s.')
    col2.write(':arrow_right: Also, the creator of this app doesn\'t support any kind of discrimination this model might do courtesy the bias prevelant over social media (as captured by the curated dataset).')
    col2.write(':arrow_right: Also, the model is biased to the data it has exposed to. One must appreciate that we can only scrape a limited chunk of Instagram data.')