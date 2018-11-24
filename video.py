import boto3
import json
import os
from image_class import video_emotion_detection

if __name__ == "__main__":

    source_bucket = 'pictureswithstudents'
    destination_bucket = 'segmentedvideo'
    video = 'video.mp4'
    fps = 1 #fps

    s3 = boto3.resource('s3')

    s3.meta.client.download_file(source_bucket, video, video)

    print('GOT VIDEO')

    os.system('ffmpeg -i '+ str(video) +' -r ' + str(fps) + ' -s 320x640 -f image2 vid%01d.jpg')
    print('DONE SAMPLING')

    numberofpics = 11
    for i in range(numberofpics):
        s3.meta.client.upload_file('vid' + str(i+1) + '.jpg', destination_bucket, 'vid' + str(i+1) + '.jpg')
        os.remove('vid' + str(i+1) + '.jpg')
        print('uploading ' + str(i) + 'out of ' + str(numberofpics) +' files')
    print('DONE UPLOADING')

    analyzer = video_emotion_detection()
    analyzer.main()
