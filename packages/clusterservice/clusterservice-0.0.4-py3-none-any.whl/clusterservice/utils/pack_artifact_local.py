import logging
import os
import sys

import tensorflow_hub as hub
from transformers import AutoModelForQuestionAnswering, AutoTokenizer

from ..controllers.ClusterService import ClusterService

logger = logging.getLogger()  # get root logger
logger.setLevel(level=logging.INFO)


def pack(sha):

    albert_model_path = os.environ['ALBERT_MODEL_PATH']
    universal_model_path = os.environ['UNIVERSAL_MODEL_PATH']

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
