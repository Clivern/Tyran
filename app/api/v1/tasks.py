# MIT License
#
# Copyright (c) 2024 Clivern
#
# This software is licensed under the MIT License. The full text of the license
# is provided below.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import time
from qdrant_client.models import PointStruct
from app.core.configs import configs
from app.core.logger import get_logger
from app.core.qdrant import Qdrant
from app.core.chroma import ChromaClient
from app.core.openai_client import OpenAIClient


def store_document_in_vector_db(document):
    log = get_logger()

    log.info(f"Store document with id {document.id} on vector database")

    if os.getenv("TEST_RUN"):
        return

    openai_client = OpenAIClient(configs.openai_api_key)
    qdrant_client = Qdrant(configs.qdrant_db_url, configs.qdrant_db_api_key)

    log.info(f"Create embedding for document with id {document.id}")

    try:
        response = openai_client.create_embedding([document.content])
    except Exception as e:
        log.error(f"Unable to create embedding: {e}")
        return

    log.info(f"Store embedding for document with id {document.id}")

    try:
        qdrant_client.insert(
            configs.qdrant_db_collection,
            [
                PointStruct(
                    id=document.id,
                    vector=response.data[0].embedding,
                    payload=document.metadata,
                )
            ],
        )
    except Exception as e:
        log.error(f"Unable to store embedding in vector database: {e}")
        return

    log.info(f"Stored embedding for document with id {document.id}")


def delete_document_from_vector_db(document_id):
    log = get_logger()

    log.info(f"Delete document with id {document_id} from the vector database")

    if os.getenv("TEST_RUN"):
        return

    print(document_id)
