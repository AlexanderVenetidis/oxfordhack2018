import boto3
import json
import os

if __name__ == "__main__":

    bucket = 'hackimp'
    fps = 5 #fps

    s3 = boto3.resource('s3')

    s3.meta.client.download_file(bucket, 'video.mp4', 'video.mp4')

    print('GOT VIDEO')

    os.system('ffmpeg -i video.mp4 -r ' + str(fps) + ' -s 320x640 -f image2 vid%01d.jpg')
    print('DONE SAMPLING')

    numberofpics = 11
    for i in range(numberofpics):
        s3.meta.client.upload_file('vid' + str(i+1) + '.jpg', bucket, 'vid' + str(i+1) + '.jpg')
        print('uploading ' + str(i) + 'out of ' + str(numberofpics) +' files')
    print('DONE UPLOADING')