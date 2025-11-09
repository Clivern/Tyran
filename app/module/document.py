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
from typing import Optional

from qdrant_client.models import PointStruct

from app.core.config import configs
from app.core.logger import get_logger
from app.model import Document, DocumentCreate, DocumentResponse
from app.repository import DocumentRepository
from app.service.openai import OpenAIClient
from app.service.qdrant import Qdrant


class DocumentModule:
    def __init__(
        self,
        document_repository: DocumentRepository,
        qdrant_client: Qdrant,
        openai_client: OpenAIClient,
    ) -> None:
        self._document_repository = document_repository
        self._qdrant_client = qdrant_client
        self._openai_client = openai_client
        self._logger = get_logger(__name__)

    def create_document(
        self,
        payload: DocumentCreate,
    ) -> DocumentResponse:
        self._logger.info("Create document with identifier %s", payload.identifier)
        document = self._document_repository.create(payload)

        self._store_document_vector(document)

        return self._build_document_response(document)

    def get_document(self, identifier: str) -> Optional[DocumentResponse]:
        document = self._document_repository.get_by_identifier(identifier)
        if document is None:
            return None

        return self._build_document_response(document)

    def delete_document(self, identifier: str) -> Optional[Document]:
        self._logger.info("Delete document with identifier %s", identifier)
        existing = self._document_repository.get_by_identifier(identifier)
        if existing is None:
            self._logger.info("Document %s not found; nothing to delete", identifier)
            return None

        deleted = self._document_repository.delete(existing.id)
        self._logger.info("Deleted document %s from persistence layer", identifier)

        self._delete_document_vector(identifier)

        return deleted

    def _build_document_response(
        self,
        document: Document,
    ) -> DocumentResponse:
        return DocumentResponse(
            id=document.identifier,
            content=document.content,
            category=document.category,
            created_at=document.created_at,
            updated_at=document.updated_at,
        )

    def _store_document_vector(
        self,
        document: Document,
    ) -> None:
        try:
            response = self._openai_client.create_embedding([document.content])
            vector = response.data[0].embedding  # type: ignore[attr-defined]
        except Exception as exc:  # noqa: BLE001
            self._logger.error(
                "Unable to create embedding for document %s: %s",
                document.identifier,
                exc,
            )
            return

        try:
            self._qdrant_client.create_collection_if_not_exist(
                configs.qdrant_db_collection
            )
            self._qdrant_client.insert(
                configs.qdrant_db_collection,
                [
                    PointStruct(
                        id=document.identifier,
                        vector=vector,
                        payload=self._build_vector_payload(document),
                    )
                ],
            )
            self._logger.info(
                "Stored vector for document %s in collection %s",
                document.identifier,
                configs.qdrant_db_collection,
            )
        except Exception as exc:  # noqa: BLE001
            self._logger.error(
                "Unable to store vector for document %s: %s",
                document.identifier,
                exc,
            )

    def _build_vector_payload(self, document: Document) -> dict[str, str]:
        index_field = (configs.qdrant_db_index or "").strip()
        if not index_field:
            return {}

        value = getattr(document, index_field, None)
        if value is None:
            self._logger.warning(
                "Document %s is missing index field %s",
                document.identifier,
                index_field,
            )
            return {}

        value_str = str(value).strip()
        if value_str == "":
            self._logger.warning(
                "Document %s has empty value for index field %s",
                document.identifier,
                index_field,
            )
            return {}

        return {index_field: value_str}

    def _delete_document_vector(self, identifier: str) -> None:
        try:
            self._qdrant_client.delete(configs.qdrant_db_collection, identifier)
            self._logger.info(
                "Deleted vector for document %s from collection %s",
                identifier,
                configs.qdrant_db_collection,
            )
        except Exception as exc:  # noqa: BLE001
            self._logger.error(
                "Unable to delete vector for document %s: %s",
                identifier,
                exc,
            )
