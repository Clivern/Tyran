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

import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.api.v1.tasks import *
from app.core.logger import Logger
from app.core import crud, schemas, database
from app.api.v1.model import Document
from app.core.logger import Logger, get_logger
from app.core.middleware import get_api_key


router = APIRouter()


@router.post("/api/v1/document", dependencies=[Depends(get_api_key)])
def create(
    doc: Document,
    bg: BackgroundTasks,
    db: Session = Depends(database.get_db),
    log: Logger = Depends(get_logger),
):
    doc.id = str(uuid.uuid4())

    log.info(f"Create a new document with id {doc.id}")

    document_create = schemas.DocumentCreate(identifier=doc.id, content=doc.content)
    created_document = crud.create_document(db=db, document=document_create)
    log.info(f"Document with id {doc.id} got created")
    doc.createdAt = created_document.created_at
    doc.updatedAt = created_document.updated_at

    for key, value in doc.metadata.items():
        log.info(f"Create meta with {key} = {value} for document {doc.id}")
        crud.create_document_meta(
            db=db,
            meta=schemas.DocumentMetaCreate(
                document_id=created_document.id, key=key, value=value
            ),
        )

    log.info(f"Trigger async job to store document with id {doc.id} data")

    bg.add_task(store_document_in_vector_db, doc)

    return doc


@router.get("/api/v1/document/{identifier}", dependencies=[Depends(get_api_key)])
def get_document_by_identifier(
    identifier: str,
    db: Session = Depends(database.get_db),
    log: Logger = Depends(get_logger),
):
    log.info(f"Fetch Document with id {identifier}")

    document = crud.get_document_by_identifier(db, identifier)

    if not document:
        log.info(f"Document with id {identifier} not found")
        raise HTTPException(status_code=404, detail=f"Document {identifier} not found")

    log.info(f"Document with id {identifier} is found")

    doc = Document(
        id=document.identifier,
        content=document.content,
        metadata={meta.key: meta.value for meta in document.meta},
        createdAt=document.created_at,
        updatedAt=document.updated_at,
    )

    return doc


@router.delete("/api/v1/document/{identifier}", dependencies=[Depends(get_api_key)])
def delete_document_by_identifier(
    identifier: str,
    bg: BackgroundTasks,
    db: Session = Depends(database.get_db),
    log: Logger = Depends(get_logger),
):
    document = crud.get_document_by_identifier(db, identifier)

    if not document:
        log.info(f"Document with id {identifier} not found")
        raise HTTPException(status_code=404, detail=f"Document {identifier} not found")

    log.info(f"Document with id {identifier} is found")
    log.info(f"Delete metas for document with id {identifier}")
    crud.delete_document_metas_by_document_id(db, document.id)
    log.info(f"Delete document with id {identifier}")
    crud.delete_document(db, document.id)

    log.info(f"Trigger async job to delete document with id {identifier}")

    bg.add_task(delete_document_from_vector_db, identifier)

    return {"detail": f"Document {identifier} deleted successfully"}
