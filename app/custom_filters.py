# custom_filters.py

from django import template
from django.conf import settings
import boto3
import hashlib


register = template.Library()

@register.filter
def md5_hash(email):
    return hashlib.md5(email.encode()).hexdigest()



@register.filter
def get_presigned_url(key):
    s3 = boto3.client('s3',
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY ,
                        region_name=settings.AWS_S3_REGION_NAME)
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME 
    expiration=10
    # Generate the pre-signed URL for the PDF file
    presigned_url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': key},ExpiresIn=expiration)
    return presigned_url