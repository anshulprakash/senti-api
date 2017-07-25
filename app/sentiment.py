import requests
import json

# Credentials for Azure Text Analytics API
apiKey = '3fdd5c46202647ab80b7ab5d117f3335'
sentimentUri = 'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment'

def getSentiment(text):

	# Prepare headers
	headers = {}
	headers['Ocp-Apim-Subscription-Key'] = apiKey
	headers['Content-Type'] = 'application/json'
	headers['Accept'] = 'application/json'

	# Determine sentiment
	postData = json.dumps({"documents":[{"id":"1", "language":'en', "text":text}]}).encode('utf-8')

	response = requests.post(sentimentUri, data = postData, headers = headers)

	#request = Request(sentimentUri, postData, headers)
	
	#response = urlopen(request)
	responsejson = json.loads(response.text.decode('utf-8'))
	sentiment = responsejson['documents'][0]['score'] # Sample json: {'errors': [], 'documents': [{'id': '1', 'score': 0.946106320818458}]}

	return sentiment