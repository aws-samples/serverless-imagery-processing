import json
import os
import boto3
import uuid
def lambda_handler(event, context):
    
    rek = boto3.client('rekognition')
    s3 = boto3.client("s3")
    
    output_bucket = os.environ['CHIP_PREDICTIONS_BUCKET']
    
    responses = []
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        img_info = {
                'S3Object':{
                    'Bucket': bucket,
                    'Name': key
                }}
        print(bucket,key)
        response = rek.detect_labels(
            Image=img_info
            )
            
        #add source image information
        
        response['source_img']= img_info
        
        #write results to s3
        
        responses.append(response)
    
    fn = str(uuid.uuid4())+'.json'
    s3.put_object(Body=json.dumps(responses), Bucket=output_bucket,Key=fn )
        
        
    return responses

