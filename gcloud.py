import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import numpy as np
from google.cloud import vision
import io
from jarowinkler import jarowinkler_similarity
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

def detect_text(image_file):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()
    print(image_file)
    # [START vision_python_migration_text_detection]
    #with io.open(path, 'rb') as image_file:
    #    content = image_file.read()

    image = vision.Image(content=image_file)

    response = client.text_detection(image=image ,image_context={"language_hints": ["es"]})  # Bengali

    texts = response.text_annotations
    print('Texts:')

    words_dict={}
    words_list=[]
    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

        words_dict[text.description]=list(vertices)
        words_list.append(text.description)
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    del words_list[0]
    return words_list

def get_dataframe():
    df = pd.read_csv("medicamentos.csv", sep=';', encoding='latin-1')
    return df

def get_prob_value(target,columna,thr):
    med = get_dataframe()
    sims =[]
    method= jarowinkler_similarity
    vocab= list(set(med[columna]))
    for word in vocab:
        sims.append(method(target, word))
    if np.max(sims) > thr:
        return vocab[np.argmax(sims)]
    else:
        return "error"

def predict(target):
    final_list = []
    for w in target:
        droga_pred= get_prob_value(w.lower() ,'Principio activo',0.8)
        gramaje_pred= get_prob_value(w.lower(),'Potencia',0.9)
        unidad_pred= get_prob_value(w.lower(),'Unidad de potencia',0.8)

        if droga_pred != "error":
            final_list.append(droga_pred)
        if gramaje_pred != "error":
            final_list.append(gramaje_pred)
        if unidad_pred != "error":
            final_list.append(unidad_pred)
    return final_list

def get_drugs(predicted_words):
    url = "https://appfarmacitymicroservice-prod.azurewebsites.net/api/Medicine/search?filter="
    for word in predicted_words:
        url = url + word + "%20"
    #print(url)

    #print('before request')
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.get(url)

    prices= []
    ids = []
    description = []
    labs = []

    for drug in response.json():
        prices.append(drug['publicPrice'])
        #ids.append(drug['id'])
        description.append(drug['description'])
        labs.append(drug['medicalLaboratory']['abbreviation'])

    df = pd.DataFrame(list(zip(description, labs, prices)), columns =['description', 'lab', 'prices'])

    return df
