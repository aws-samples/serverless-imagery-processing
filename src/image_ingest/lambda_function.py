import json
import os
import boto3


def lambda_handler(event, context):
    # get duplicate chipper count
    num_chippers = int(os.environ['DUPLICATE_CHIPPERS'])
    
    queue_name = os.environ['OUTPUT_QUEUE']
    
    SQS = boto3.resource('sqs')
    q = SQS.get_queue_by_name(QueueName=queue_name)
    

    
    # for each record iterate through num_chippers and create an entry for each 
    # future chipper
    
    images_to_chip=[]
    for i in range(num_chippers):
        for record in event['Records']:
            new_record = record.copy()
            new_record['chipperID'] = i
            new_record['numChippers']= num_chippers
            images_to_chip.append(new_record)
            r = q.send_message(MessageBody=json.dumps(new_record))
            print(r)
    
    return images_to_chip
