#function emotion_detection
#assume the text to be analysed is passed to the function as an argument
# stored in text_to_analyze
# returned in the text attribute of the function

import requests
import json

def emotion_detection(text_to_analyze):
    # endpoint provided by the lab intructions 
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"

    # header 
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    # The payload containing the text you want to check
    myobj = { "raw_document": { "text": text_to_analyze } }

    #sending the post request to the endpoint
    response = requests.post(url, json = myobj, headers = header)

    #returning the text attribute of the response
    return response.text