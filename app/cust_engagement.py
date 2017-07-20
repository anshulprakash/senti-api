from watson_developer_cloud import ToneAnalyzerV3
import json

u_name = '08aa7b52-622d-4de2-a8bd-d6e0ffcf3ba7'#raw_input('[Tone analysis] Enter the user name: ')
p_wd = 'xNNYNJsjG1LB' #raw_input('[Tone analysis] Enter the password: ')
 
tone_analyzer = ToneAnalyzerV3(
  username=u_name,
  password=p_wd,
  version='2016-02-11'
)
'''
	This method is used to get use the customer engagement end point of IBM's Tone Analyzer
'''
def getUtteranceAnalysis(utterances_dict):

    tone = tone_analyzer.tone_chat(utterances_dict['utterances'])

    return json.dumps(tone)