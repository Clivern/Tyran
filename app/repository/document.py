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

from __future__ import annotations
from typing import Iterable, List, Optional

from sqlalchemy.orm import Session

from app.db import scheme
from app.model import Document, DocumentCreate


class DocumentRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, document: DocumentCreate) -> Document:
        db_document = scheme.Document(**document.model_dump())
        self._session.add(db_document)
        self._session.commit()
        self._session.refresh(db_document)
        return Document.model_validate(db_document)

    def get(self, document_id: int) -> Optional[Document]:
        db_document = (
            self._session.query(scheme.Document)
            .filter(scheme.Document.id == document_id)
            .first()
        )
        return Document.model_validate(db_document) if db_document else None

    def get_by_identifier(self, identifier: str) -> Optional[Document]:
        db_document = (
            self._session.query(scheme.Document)
            .filter(scheme.Document.identifier == identifier)
            .first()
        )
        return Document.model_validate(db_document) if db_document else None

    def list_by_identifiers(self, identifiers: Iterable[str]) -> List[Document]:
        identifiers = list(identifiers)
        if not identifiers:
            return []
        documents = (
            self._session.query(scheme.Document)
            .filter(scheme.Document.identifier.in_(identifiers))
            .all()
        )
        return [Document.model_validate(document) for document in documents]

    def delete(self, document_id: int) -> Optional[Document]:
        db_document = (
            self._session.query(scheme.Document)
            .filter(scheme.Document.id == document_id)
            .first()
        )
        if db_document is None:
            return None
        self._session.delete(db_document)
        self._session.commit()
        return Document.model_validate(db_document)
