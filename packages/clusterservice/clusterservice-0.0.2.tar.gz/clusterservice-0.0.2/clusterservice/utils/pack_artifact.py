import logging
import os
import sys

import boto3
import tensorflow_hub as hub
from botocore.client import Config
from transformers import AutoModelForQuestionAnswering, AutoTokenizer

from controllers.ClusterService import ClusterService

logger = logging.getLogger()  # get root logger
logger.setLevel(level=logging.INFO)


def pack(sha):
    s3 = boto3.resource('s3',
        endpoint_url=os.environ['S3_ENDPOINT_URL'],
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        config=Config(signature_version='s3v4'),
        region_name='us-east-1'
    )

    def download_directory(bucket_name, directory, local_directory=None):
        if local_directory is None:
            local_directory = os.path.join('/tmp', bucket_name, directory)

        if not os.path.exists(local_directory):
            os.makedirs(local_directory)

        bucket = s3.Bucket(bucket_name)
        for obj in bucket.objects.filter(Prefix=directory):
            target = os.path.join(local_directory, os.path.relpath(obj.key, directory))
            if not os.path.exists(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            if obj.key[-1] == '/':
                continue
            bucket.download_file(obj.key, target)

    albert_model_path = '/tmp/models/albert-xlarge-v2-squad-v2'
    universal_model_path = '/tmp/models/universal-sentence-encoder_4'

    if not os.path.exists(universal_model_path):
        download_directory('models', 'universal-sentence-encoder_4')

    if not os.path.exists(albert_model_path):
        download_directory('models', 'albert-xlarge-v2-squad-v2')

    svc = ClusterService()

    model = AutoModelForQuestionAnswering.from_pretrained(albert_model_path)
    tokenizer = AutoTokenizer.from_pretrained(albert_model_path)
    embedder = hub.load(universal_model_path)

    svc.pack('albert', { 'model': model, 'tokenizer': tokenizer })
    svc.pack('embedder', { 'embedder': embedder })

    saved_path = svc.save(labels={'sha': sha})

    print(saved_path)
    return saved_path


if __name__ == '__main__':
    sha = str(sys.argv[1]) if len(sys.argv) == 2 else ''
    pack(sha)
