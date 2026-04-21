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

    try:
        #sending the post request to the endpoint
        response = requests.post(url, json = myobj, headers = header, timeout = 10)
        response.raise_for_status()

        #returning the text attribute of the response
        return response.text
    except requests.RequestException as error:
        return f"Error: {error}"
    
    #1. convert the response text to json format
    formatted_response = json.loads(response.text)

    #2. extract the emotions from the specific path in the JSON structure 
    # The watson response stores emotions under 'emotionPrediction' -> 'emotion'
    emotions = formatted_response['emotionPrediction'][0]['emotion']

    anger_store = emotions['anger']
    disgust_store = emotions['disgust']
    fear_store = emotions['fear']
    joy_store = emotions['joy']
    sadness_store = emotions['sadness']

    #3. Find the dominant emotion (highest score)
    dominant_emotion = max(emotions, key=emotions.get)

    #4. Return the specific format requested 
    return {
        'anger': anger_store,
        'disgust': disgust_store,
        'fear': fear_store,
        'joy': joy_store,
        'sadness': sadness_store,
        'dominant_emotion': dominant_emotion
    }