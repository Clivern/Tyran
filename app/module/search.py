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

from typing import List

from app.core.config import configs
from app.core.logger import get_logger
from app.model import DocumentSearchResult
from app.repository import DocumentRepository
from app.service.openai import OpenAIClient
from app.service.qdrant import Qdrant


class SearchModule:
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

    def search_documents(
        self,
        query: str,
        category: str,
        limit: int = 5,
    ) -> List[DocumentSearchResult]:
        category_value = category.strip()

        self._logger.info(
            "Search documents for query %s in category %s with limit %s",
            query,
            category_value,
            limit,
        )

        try:
            response = self._openai_client.create_embedding([query])
            vector = response.data[0].embedding  # type: ignore[attr-defined]
        except Exception as exc:  # noqa: BLE001
            self._logger.error(
                "Unable to create embedding for query %s: %s", query, exc
            )
            return []

        try:
            results = self._qdrant_client.search(
                configs.qdrant_db_collection,
                vector,
                metadata={configs.qdrant_db_index: category_value},
                limit=limit,
            )
        except Exception as exc:  # noqa: BLE001
            self._logger.error("Vector search failed for query %s: %s", query, exc)
            return []

        if not results:
            self._logger.info("No search results found for query %s", query)
            return []

        identifiers = [str(result["id"]) for result in results]
        documents = self._document_repository.list_by_identifiers(identifiers)
        documents_map = {document.identifier: document for document in documents}

        search_results: List[DocumentSearchResult] = []

        for result in results:
            identifier = str(result["id"])
            document = documents_map.get(identifier)

            if document is None:
                self._logger.warning(
                    "Document %s returned by vector search but not found in repository",
                    identifier,
                )
                continue

            search_results.append(
                DocumentSearchResult(
                    id=document.identifier,
                    content=document.content,
                    category=document.category,
                    created_at=document.created_at,
                    updated_at=document.updated_at,
                    score=float(result.get("score", 0.0)),
                )
            )

        return search_results
