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

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_home_endpoint():
    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_endpoint():
    # Act
    response = client.get("/_health")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_endpoint():
    # Act
    response = client.get("/_ready")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_store_document_endpoint():
    # Act
    response = client.post(
        "/api/v1/document",
        json={
            "content": "Hello World",
            "metadata": {"author": "John Doe", "category": "Test"},
        },
    )

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["content"] == "Hello World"
    assert response_data["metadata"] == {"author": "John Doe", "category": "Test"}
    assert "createdAt" in response_data
    assert "updatedAt" in response_data


def test_get_document_by_identifier_success():
    # Arrange
    response = client.post(
        "/api/v1/document",
        json={
            "content": "Hello World",
            "metadata": {"author": "John Doe", "category": "Test"},
        },
    )
    response_data = response.json()
    document_id = response_data["id"]

    # Act
    response = client.get(f"/api/v1/document/{document_id}")

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == document_id
    assert response_data["content"] == "Hello World"
    assert response_data["metadata"] == {"author": "John Doe", "category": "Test"}
    assert "createdAt" in response_data
    assert "updatedAt" in response_data


def test_get_document_by_identifier_not_found():
    # Act
    response = client.get("/api/v1/document/non_existent_doc")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Document non_existent_doc not found"}


def test_delete_document_by_identifier_success():
    # Arrange
    response = client.post(
        "/api/v1/document",
        json={
            "content": "Hello World",
            "metadata": {"author": "John Doe", "category": "Test"},
        },
    )
    response_data = response.json()
    document_id = response_data["id"]

    # Act
    response = client.delete(f"/api/v1/document/{document_id}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"detail": f"Document {document_id} deleted successfully"}


def test_delete_document_by_identifier_not_found():
    # Act
    response = client.delete("/api/v1/document/non_existent_doc")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Document non_existent_doc not found"}
