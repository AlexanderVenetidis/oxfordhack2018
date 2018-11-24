import boto3
import json


def splitter(n, s):
    pieces = s.split(". ")
    return (". ".join(pieces[i:i+n]) for i in range(0, len(pieces), n))

s3 = boto3.resource('s3',
                    aws_access_key_id='AKIAJAIFD4JMQBHLQCCQ',
                    aws_secret_access_key='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')
content_object = s3.Object('speech-result-1234567', 'speech1.json')
file_content = content_object.get()['Body'].read().decode('utf-8')
json_content = json.loads(file_content)


comprehend = boto3.client(service_name='comprehend')





text = str(json_content['results']['transcripts'][0]['transcript'])

for piece in splitter(50, text):
    print(piece)
    print('Calling DetectDominantLanguage')
    print(json.dumps(comprehend.detect_sentiment(Text=piece, LanguageCode='en'), sort_keys=True, indent=4))
    print("End of DetectDominantLanguage\n")


