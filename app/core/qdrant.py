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

from qdrant_client import QdrantClient, models
from qdrant_client.models import VectorParams, Distance
from app.core.configs import configs


class Qdrant:
    def __init__(self, qdrant_url, qdrant_api_key):
        self._client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

    def create_collection_if_not_exist(self, collection: str, size=1536):
        if not self._client.collection_exists(collection):
            self._client.create_collection(
                collection,
                vectors_config=VectorParams(size=size, distance=Distance.COSINE),
            )

    def insert(self, collection: str, points: list):
        return self._client.upsert(collection, points)

    def search(self, collection, query_vector, metadata={}, limit=1):
        must = []

        for key, value in metadata.items():
            must.append(
                models.FieldCondition(
                    key=key,
                    match=models.MatchValue(
                        value=value,
                    ),
                )
            )

        if len(must) > 0:
            results = self._client.search(
                collection_name=collection,
                query_vector=query_vector,
                query_filter=models.Filter(must=must),
                limit=limit,
            )
        else:
            results = self._client.search(
                collection_name=collection, query_vector=query_vector, limit=limit
            )

        data = []

        for result in results:
            data.append({"id": result.id, "score": result.score})

        return data

    def delete(self, collection: str, document_id: str):
        return self._client.delete(
            collection_name=collection,
            points_selector=models.PointIdsList(
                points=[document_id],
            ),
        )


def get_qdrant() -> Qdrant:
    return Qdrant(configs.qdrant_db_url, configs.qdrant_db_api_key)
