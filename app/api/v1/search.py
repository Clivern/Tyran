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

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.configs import configs
from app.core.logger import Logger
from app.api.v1.model import RelatedDocument
from app.api.v1.model import Prompt
from app.core import crud, schemas, database
from app.core.logger import Logger, get_logger
from app.core.qdrant import Qdrant, get_qdrant
from app.core.openai_client import OpenAIClient, get_openai_client


router = APIRouter()


@router.post("/api/v1/document/search")
def search(
    prompt: Prompt,
    db: Session = Depends(database.get_db),
    log: Logger = Depends(get_logger),
    openai_client: OpenAIClient = Depends(get_openai_client),
    qdrant_client: Qdrant = Depends(get_qdrant),
):
    log.info(f"Create embedding for prompt `{prompt.text}`")

    try:
        response = openai_client.create_embedding([prompt.text])
    except Exception as e:
        log.error(f"Unable to create embedding: {e}")
        raise Exception("Internal Server Error")

    log.info(f"Query vector database for similar records")

    try:
        idents = qdrant_client.search(
            configs.qdrant_db_collection,
            response.data[0].embedding,
            prompt.metadata,
            prompt.limit,
        )
    except Exception as e:
        log.error(f"Unable to find related documents: {e}")
        raise Exception("Internal Server Error")

    if len(idents) == 0:
        log.info(f"No similar documents is found")
        return []

    log.info(f"Fetch similar documents {idents}")

    try:
        documents = crud.get_documents_by_identifiers(
            db, [param["id"] for param in idents]
        )
    except Exception as e:
        log.error(f"Unable to fetch related documents from database: {e}")
        raise Exception("Internal Server Error")

    result = []
    score_map = {item["id"]: item["score"] for item in idents}

    log.info(f"Build a final output for {idents}")

    for document in documents:
        result.append(
            RelatedDocument(
                id=document.identifier,
                score=score_map[document.identifier],
                content=document.content,
                metadata={meta.key: meta.value for meta in document.meta},
                createdAt=document.created_at,
                updatedAt=document.updated_at,
            )
        )

    result.sort(key=lambda x: x.score, reverse=True)

    return result
