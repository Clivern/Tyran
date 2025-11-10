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

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.deps import get_document_module
from app.model import DocumentCreate, DocumentCreateRequest, DocumentResponse
from app.module import DocumentModule

router = APIRouter()


@router.post(
    "/document",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_document(
    request: DocumentCreateRequest,
    document_module: DocumentModule = Depends(get_document_module),
) -> DocumentResponse:
    document_payload = DocumentCreate(
        identifier=str(uuid4()),
        content=request.content,
        category=request.category.strip(),
    )
    return document_module.create_document(document_payload)


@router.get("/document/{identifier}", response_model=DocumentResponse)
def get_document(
    identifier: str,
    document_module: DocumentModule = Depends(get_document_module),
) -> DocumentResponse:
    document = document_module.get_document(identifier)
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )
    return document
