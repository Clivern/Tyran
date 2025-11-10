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
from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.client import get_db as _get_db
from app.module import DocumentModule, SearchModule
from app.repository.document import DocumentRepository
from app.repository.option import OptionRepository
from app.service import OpenAIClient, Qdrant, get_openai_client, get_qdrant


def get_db() -> Generator[Session, None, None]:
    yield from _get_db()


def get_option_repository(
    session: Session = Depends(get_db),
) -> OptionRepository:
    return OptionRepository(session)


def get_document_repository(
    session: Session = Depends(get_db),
) -> DocumentRepository:
    return DocumentRepository(session)


def get_document_module(
    document_repository: DocumentRepository = Depends(get_document_repository),
    qdrant_client: Qdrant = Depends(get_qdrant),
    openai_client: OpenAIClient = Depends(get_openai_client),
) -> DocumentModule:
    return DocumentModule(
        document_repository,
        qdrant_client,
        openai_client,
    )


def get_search_module(
    document_repository: DocumentRepository = Depends(get_document_repository),
    qdrant_client: Qdrant = Depends(get_qdrant),
    openai_client: OpenAIClient = Depends(get_openai_client),
) -> SearchModule:
    return SearchModule(
        document_repository,
        qdrant_client,
        openai_client,
    )
