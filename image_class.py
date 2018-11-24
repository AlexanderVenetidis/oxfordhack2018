#
# import boto3
# import json
#
# if __name__ == "__main__":
#     photo='bored1.jpg'
#     bucket='pictureswithstudents'
#     client=boto3.client('rekognition')
#
#     response = client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':photo}},Attributes=['ALL'])
#
#     print('Detected faces for ' + photo)
#     for faceDetail in response['FaceDetails']:
#         print('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
#               + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
#         print('Here are the other attributes:')
#         print(json.dumps(faceDetail, indent=4, sort_keys=True))

#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)



import boto3
import json

class video_emotion_detection:

    s3 = boto3.resource('s3')

    bucket='segmentedvideo'
    my_bucket = s3.Bucket(bucket)

    client=boto3.client('rekognition')


    TimeWindowLength = 3
    SamplingPeriod = 1

    SamplesPerBatch = TimeWindowLength/SamplingPeriod

    Windows = []
    PreviousFaceNum = 9999
    MaxFaces = 0
    BatchConfused = BatchBored = BatchDistracted = 0

    def __init__(self):
        pass






    def AnalyzeFaces(self, response, PreviousFaceNum):
        '''
        Takes (response, PreviousFaceNum)
        returns tuple containing (NumFaces, ConfusedPeople, BoredPeople, DistractedPeople)
        '''



        ConfusedPeople = 0
        BoredPeople = 0
        DistractedPeople = 0



        for faceDetail in response['FaceDetails']:
            for count, emotions in enumerate(faceDetail['Emotions']):
                if emotions['Type'] == 'DISGUSTED':
                    DISGUSTED = count
                elif emotions['Type'] == 'HAPPY':
                    HAPPY = count
                elif emotions['Type'] == 'SURPRISED':
                    SURPRISED = count
                elif emotions['Type'] == 'ANGRY':
                    ANGRY = count
                elif emotions['Type'] == 'CONFUSED':
                    CONFUSED = count
                elif emotions['Type'] == 'CALM':
                    CALM = count
                elif emotions['Type'] == 'SAD':
                    SAD = count



            if (faceDetail['Emotions'][CONFUSED]['Confidence'] > 80) or  (faceDetail['Emotions'][DISGUSTED]['Confidence'] > 80):
                ConfusedPeople += 1


            if ( ((faceDetail['Emotions'][CALM]['Confidence'] > 75) and
               (faceDetail['Emotions'][HAPPY]['Confidence'] < 20) and
               (faceDetail['Emotions'][SURPRISED]['Confidence'] < 20) and
               (faceDetail['Emotions'][ANGRY]['Confidence'] < 20) and
               (faceDetail['Emotions'][CONFUSED]['Confidence'] < 20) and
               (faceDetail['Emotions'][SAD]['Confidence'] < 20) and
               (faceDetail['Emotions'][DISGUSTED]['Confidence'] < 20)) or
               (faceDetail['EyesOpen']['Value'] == 'false' and faceDetail['EyesOpen']['Confidence'] > 80) ):
               BoredPeople += 1

            if (len(response['FaceDetails']) < PreviousFaceNum):
                if (PreviousFaceNum != 9999):
                    DistractedPeople = PreviousFaceNum - len(response['FaceDetails'])
            PreviousFaceNum = len(response['FaceDetails'])

            if ((faceDetail['MouthOpen']['Value'] == 'true' and faceDetail['Confidence'] > 80) or
               (faceDetail['EyesOpen']['Value'] == 'false' and faceDetail['EyesOpen']['Confidence'] > 80) or
               (abs(faceDetail['Pose']['Yaw']) > 60)):
                DistractedPeople += 1


        return (len(response['FaceDetails']), ConfusedPeople, BoredPeople, DistractedPeople)

    def main(self):
        counter = 0
        BatchConfused = BatchBored = BatchDistracted = 0


        for file in self.my_bucket.objects.all():
            counter += 1

            photo=file.key

            response = self.client.detect_faces(Image={'S3Object':{'Bucket':self.bucket,'Name':photo}},Attributes=['ALL'])

            NumFaces, ConfusedPeople, BoredPeople, DistractedPeople = self.AnalyzeFaces(response, self.PreviousFaceNum)

            if (NumFaces > self.MaxFaces):
                self.MaxFaces = NumFaces

            BatchConfused += ConfusedPeople
            BatchBored += BoredPeople
            BatchDistracted += DistractedPeople

            if counter % self.SamplesPerBatch == 0:
                self.Windows.append({'AvgConfused': float(BatchConfused)/self.SamplesPerBatch,
                                'AvgBored': float(BatchBored)/self.SamplesPerBatch,
                                'AvgDistracted': float(BatchDistracted)/self.SamplesPerBatch})
                BatchConfused = BatchBored = BatchDistracted = 0
        print(self.Windows)
