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

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from .client import Base


class Option(Base):
    __tablename__ = "option"

    id = Column(Integer, primary_key=True)
    key = Column(String(60), unique=True, index=True)
    value = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), default=func.now())

    def __repr__(self):
        return f"<Option(id={self.id}, key={self.key})>"


class Document(Base):
    __tablename__ = "document"

    id = Column(Integer, primary_key=True)
    identifier = Column(String(60), unique=True, index=True)
    category = Column(String(60), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), default=func.now())

    # Relationship to access metadata associated with the document
    meta = relationship("DocumentMeta", back_populates="document")

    def __repr__(self):
        return f"<Document(id={self.id}, identifier={self.identifier})>"


class DocumentMeta(Base):
    __tablename__ = "document_meta"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("document.id"), nullable=False)
    key = Column(String(60), index=True, nullable=False)
    value = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), default=func.now())

    # Relationship to access the associated document
    document = relationship("Document", back_populates="meta")

    def __repr__(self):
        return f"<DocumentMeta(id={self.id}, document_id={self.document_id}, key={self.key})>"
