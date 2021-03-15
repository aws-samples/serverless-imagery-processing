import json
import os
from PIL import Image
from io import BytesIO
import boto3

def lambda_handler(event, context):
    #print(event)
    x_stride = int(os.environ['STRIDE_X_DIM'])
    y_stride = int(os.environ['STRIDE_Y_DIM'])
    
    window_x = int(os.environ['WINDOW_X_DIM'])
    window_y = int(os.environ['WINDOW_Y_DIM'])
    
    chip_bucket = os.environ['CHIP_BUCKET']
    chip_info_bucket = os.environ['CHIP_INFO_BUCKET']
    
    
    
    #download image
    #this assumes the batch size is 1
    record = json.loads(event['Records'][0]['body'])
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']
    
    s3 = boto3.client("s3")
   

    
    img_data = BytesIO()
    s3.download_fileobj(bucket, key, img_data)
    img_data.seek(0)
    
    #load image with pil
    im = Image.open(img_data)
    
    
    #get which chips to write out
    numChippers = record['numChippers']
    chipperID = record['chipperID']
    print('init chipper', numChippers, chipperID, key)
    #get image dims
    width, height = im.size
    print('w,h', width, height)
    image_idx =0
    
    file_id = os.path.splitext(key)[0]
    
    #client = boto3.client('s3')
    chip_records = []
    for x in range(0, width, x_stride): #this does not account for final partial chip
        for y in range(0, height, y_stride):
            if image_idx % numChippers ==chipperID:
                chip_record ={}
                #chip the image
                chip = im.crop((x,y, x+window_x, y+window_y))
                
                #write chip to S3
                chipname = f"{file_id}_{image_idx}.png"
                print(chipperID, 'writing chip', image_idx)
                img_buf = BytesIO()
                chip.save(img_buf, 'PNG')
                s3.put_object(Body=img_buf.getvalue(), Bucket=chip_bucket,Key=chipname )
                
                #write info to s3
                chip_record=record.copy()
                chip_record['chipname']= chipname
                chip_record['chip_bucket']=chip_bucket
                chip_record['x_stride']= x_stride
                chip_record['y_stride']= y_stride
                chip_record['x_window']= window_x
                chip_record['y_window']= window_y
                chip_record['orig_x']= x
                chip_record['orig_y']= y
                chip_infoname = f"{file_id}_{image_idx}.json"
                s3.put_object(Body=json.dumps(chip_record), Bucket=chip_info_bucket,Key=chip_infoname )

            image_idx +=1
    
    print(bucket, key)
    
    return chip_records
