from __future__ import print_function
import time
import boto3
transcribe = boto3.client('transcribe')
job_name = "speech1"
job_uri = "https://s3.amazonaws.com/speech-recog-12345/dnc-2004-speech.mp4"
transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': job_uri},
    MediaFormat='mp4',
    LanguageCode='en-US',
    OutputBucketName='speech-result-1234567'
)
while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print("Not ready yet...")
    time.sleep(5)


print(status)