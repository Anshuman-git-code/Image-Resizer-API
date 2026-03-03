import json
import boto3
from PIL import Image
import io
import os

s3 = boto3.client('s3')

SOURCE_BUCKET = os.environ['SOURCE_BUCKET']
DEST_BUCKET = os.environ['DEST_BUCKET']

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        image_key = body['image_key']
        width = int(body.get('width', 300))
        height = int(body.get('height', 300))

        response = s3.get_object(Bucket=SOURCE_BUCKET, Key=image_key)
        image = Image.open(io.BytesIO(response['Body'].read()))

        resized = image.resize((width, height))

        buffer = io.BytesIO()
        resized.save(buffer, format="JPEG")

        new_key = f"resized-{image_key}"

        s3.put_object(
            Bucket=DEST_BUCKET,
            Key=new_key,
            Body=buffer.getvalue(),
            ContentType="image/jpeg"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Image resized successfully",
                "output_key": new_key
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
