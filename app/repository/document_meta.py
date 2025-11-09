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
from typing import List, Optional

from sqlalchemy.orm import Session

from app.db import scheme
from app.model import (
    DocumentMeta,
    DocumentMetaCreate,
)


class DocumentMetaRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, meta: DocumentMetaCreate) -> DocumentMeta:
        db_meta = scheme.DocumentMeta(**meta.model_dump())
        self._session.add(db_meta)
        self._session.commit()
        self._session.refresh(db_meta)
        return DocumentMeta.model_validate(db_meta)

    def get(self, meta_id: int) -> Optional[DocumentMeta]:
        db_meta = (
            self._session.query(scheme.DocumentMeta)
            .filter(scheme.DocumentMeta.id == meta_id)
            .first()
        )
        return DocumentMeta.model_validate(db_meta) if db_meta else None

    def list_by_document(self, document_id: int) -> List[DocumentMeta]:
        metas = (
            self._session.query(scheme.DocumentMeta)
            .filter(scheme.DocumentMeta.document_id == document_id)
            .all()
        )
        return [DocumentMeta.model_validate(meta) for meta in metas]

    def delete(self, meta_id: int) -> Optional[DocumentMeta]:
        db_meta = (
            self._session.query(scheme.DocumentMeta)
            .filter(scheme.DocumentMeta.id == meta_id)
            .first()
        )
        if db_meta is None:
            return None
        self._session.delete(db_meta)
        self._session.commit()
        return DocumentMeta.model_validate(db_meta)

    def delete_by_document(self, document_id: int) -> List[DocumentMeta]:
        metas = (
            self._session.query(scheme.DocumentMeta)
            .filter(scheme.DocumentMeta.document_id == document_id)
            .all()
        )
        if not metas:
            return []
        for meta in metas:
            self._session.delete(meta)
        self._session.commit()
        return [DocumentMeta.model_validate(meta) for meta in metas]
