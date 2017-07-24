from app import app
from flask import Flask, request, session
import json
import tone
import cust_engagement
from textblob import TextBlob


@app.route('/')
def main():
    return "Welcome"

app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

def sumSessionCounter():
  try:
    session['counter'] += 1
  except KeyError:
    session['counter'] = 1

'''
This end-point URL will be used to get tone for the text
@param text
'''
@app.route('/Tone', methods=['POST'])
def Tone():

    obj = {}
    obj["text"] = str(request.values.get("text"))

    toneanalysis = json.loads(tone.getTone(obj["text"]))
    
    # parsing tone analysis json object to get relevant fields
    anger = toneanalysis['document_tone']['tone_categories'][0]['tones'][0]['tone_name']
    anger_score = toneanalysis['document_tone']['tone_categories'][0]['tones'][0]['score']
    disgust = toneanalysis['document_tone']['tone_categories'][0]['tones'][1]['tone_name']
    disgust_score = toneanalysis['document_tone']['tone_categories'][0]['tones'][1]['score']
    fear = toneanalysis['document_tone']['tone_categories'][0]['tones'][2]['tone_name']
    fear_score = toneanalysis['document_tone']['tone_categories'][0]['tones'][2]['score']
    joy = toneanalysis['document_tone']['tone_categories'][0]['tones'][3]['tone_name']
    joy_score = toneanalysis['document_tone']['tone_categories'][0]['tones'][3]['score']
    sadness = toneanalysis['document_tone']['tone_categories'][0]['tones'][4]['tone_name']
    sadness_score = toneanalysis['document_tone']['tone_categories'][0]['tones'][4]['score']

    # creating a json object for the tones and their corresponding scores
    data = {anger : anger_score, disgust : disgust_score, fear : fear_score, joy : joy_score, sadness : sadness_score}

    return json.dumps(data)

'''
This end-point URL will be used to get contextual analysis
@param: user
@param: text
@param: start a flag to notify if a conversation is starting
'''
@app.route('/Contextual', methods=['POST'])
def Contextual():
    
    #if the start flag is set to yes then clear the session
    if(request.values.get("start").lower() == 'yes'):
        session.clear()

    sumSessionCounter()

    temp_dict = {"text": str(request.values.get("text")), 
                 "user": str(request.values.get("user"))}
    
    #If session's utterance dictionary is not set then initialize it otherwise append the new utterance to list of utterances
    try:
        utterance_dict = session['utterance_dict']
        utterance_dict['utterances'].append(temp_dict)
        session['utterance_dict'] = utterance_dict
    except KeyError:
        session['utterance_dict'] = { "utterances": [ temp_dict ] }

    return cust_engagement.getUtteranceAnalysis(session['utterance_dict'])

'''
This end-point URL will be used to get sentiment for a text
@param: text

'''
@app.route('/Sentiment', methods=['POST'])
def Sentiment():
    
    text = request.values.get("text")
    # create TextBlob object of passed tweet text
    analysis = TextBlob(self.clean_tweet(text))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


