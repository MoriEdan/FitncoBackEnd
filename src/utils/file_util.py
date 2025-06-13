# -*- coding: utf-8 -*-

import datetime
import logging
import os
import shutil
import uuid

import boto3
import requests
from botocore.exceptions import ClientError
from flask import current_app


def allowed_file(filename):
    extensions = current_app.config["ALLOWED_EXTENSIONS"]
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in extensions


def upload_file(file_name, content_type, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    date_path = datetime.date.today().strftime('%Y_%m_%d') + '/' + object_name

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
    )
    try:
        args = {'ContentType': content_type}
        s3_client.upload_file(file_name, current_app.config['AWS_BUCKET'], date_path, ExtraArgs=args)
        url = f'https://{current_app.config["AWS_BUCKET"]}.s3.amazonaws.com/{date_path}'
        return url
    except ClientError as e:
        logging.error(e)
        return None
    except Exception as e:
        print(e)
        return None


def download_file(url, file_name):
    res = requests.get(url, stream=True)
    path = f'media/{file_name}'
    content_type = res.headers['Content-Type']
    if res.status_code == 200:
        with open(path, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
            f.close()
        resp = requests.post(f"https://fitco.mindary.online/api/test", files={'file': open(path, 'rb'), 'Content-Type': content_type})
        url = resp.json()['data']
        return url
