import requests
import json


def _empty_emotion_result():
    return {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None,
    }

def emotion_detector(text_to_analyze):
    URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }
    
    try:
        response = requests.post(URL, json = input_json, headers=header, timeout=10)
        formated_response = json.loads(response.text)

        if response.status_code == 200:
            return formated_response
        elif response.status_code == 400:
            return _empty_emotion_result()
    except requests.exceptions.RequestException:
        return _empty_emotion_result()

def emotion_predictor(detected_text):
    if all(value is None for value in detected_text.values()):
        return detected_text
    if detected_text['emotionPredictions'] is not None:
        emotions = detected_text['emotionPredictions'][0]['emotion']
        anger = emotions['anger']
        disgust = emotions['disgust']
        fear = emotions['fear']
        joy = emotions['joy']
        sadness = emotions['sadness']
        max_emotion = max(emotions, key=emotions.get)
        #max_emotion_score = emotions[max_emotion]
        formated_dict_emotions = {
                                'anger': anger,
                                'disgust': disgust,
                                'fear': fear,
                                'joy': joy,
                                'sadness': sadness,
                                'dominant_emotion': max_emotion
                                }
        return formated_dict_emotions


def format_emotion_report(result, analyzed_text=None):
    if not result or result.get('dominant_emotion') is None:
        return 'Emotion report: unavailable (service/network issue).'

    lines = ['Emotion Report']
    if analyzed_text:
        lines.append(f'Text: "{analyzed_text}"')
    lines.append(f"Dominant emotion: {result['dominant_emotion'].upper()}")
    lines.append('Scores:')
    lines.append(f"  anger   : {result['anger']:.4f}")
    lines.append(f"  disgust : {result['disgust']:.4f}")
    lines.append(f"  fear    : {result['fear']:.4f}")
    lines.append(f"  joy     : {result['joy']:.4f}")
    lines.append(f"  sadness : {result['sadness']:.4f}")
    return '\n'.join(lines)


if __name__ == '__main__':
    user_text = input('Enter text to analyze: ').strip()
    detected = emotion_detector(user_text)
    result = emotion_predictor(detected)
    print(format_emotion_report(result, user_text))