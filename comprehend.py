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


n = 0
text_each_minute = ""
word = ""
count = 1
time = 0.0
time_windows = []


while n < len(json_content['results']['items']):
    word = str(json_content['results']['items'][n]["alternatives"][0]["content"])
    if str(json_content['results']['items'][n]["type"]) != "punctuation":
        time = float(str(json_content['results']['items'][n]['end_time']))
    if time/60 <= count:
        if word == "." or word == ",":
            text_each_minute = text_each_minute[:-1] + word + " "
        else:
            text_each_minute = text_each_minute + word + " "
        n += 1
    else:
        if word == ".":
            information = json.loads(json.dumps(comprehend.detect_sentiment(Text=text_each_minute, LanguageCode='en'), sort_keys=True, indent=4))
            time_windows.append(information["SentimentScore"])
            text_each_minute = ""
            count += 1
            n += 1
        else:
            while word != ".":
                n += 1
                word = str(json_content['results']['items'][n]["alternatives"][0]["content"])
                if word == "." or word == ",":
                    text_each_minute = text_each_minute[:-1] + word + " "
                else:
                    text_each_minute = text_each_minute + word + " "


        information = json.loads(json.dumps(comprehend.detect_sentiment(Text=text_each_minute, LanguageCode='en'), sort_keys=True,
                                 indent=4))
        time_windows.append(information["SentimentScore"])
        text_each_minute = ""
        count += 1


print('show sentiment')
information = json.loads(json.dumps(comprehend.detect_sentiment(Text=text_each_minute, LanguageCode='en'), sort_keys=True, indent=4))
time_windows.append(information["SentimentScore"])
print(time_windows)
print("show sentiment\n")






