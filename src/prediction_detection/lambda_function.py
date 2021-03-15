import json
import os
import boto3
from io import BytesIO
def lambda_handler(event, context):
    queue_name = os.environ['PREDICTION_QUEUE']
    chip_info_bucket = os.environ['CHIP_INFO_BUCKET']
    SQS = boto3.resource('sqs')
    q = SQS.get_queue_by_name(QueueName=queue_name)

    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        #download file 
        s3 = boto3.client("s3")
        file_data = BytesIO()
        s3.download_fileobj(bucket, key, file_data)
        file_data.seek(0)
        
        j = json.load(file_data)
        
        
        
        for pred in j:
            #get chip name so we can find the info file in s3 and merge them
            
            #this is the only mandatory information that must be inserted
            # in the prediction so the flow works
            chip_name = pred['source_img']['S3Object']['Name']
            
            file_data = BytesIO()
            info_file = chip_name[:-4] +'.json'
            print(chip_info_bucket, info_file)
            
            s3.download_fileobj(chip_info_bucket, info_file, file_data)
            file_data.seek(0)
            chip_info = json.load(file_data)
            
            pred['chip_info']= chip_info
            r = q.send_message(MessageBody=json.dumps(pred))
            print(r)    
        #there may be multiple predictions per file
        # this is specific for rekognition output

    return event

