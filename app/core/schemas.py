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

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Option schemas
class OptionBase(BaseModel):
    key: str
    value: str


class OptionCreate(OptionBase):
    pass


class OptionUpdate(BaseModel):
    key: Optional[str] = None
    value: Optional[str] = None


class Option(OptionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Document schemas
class DocumentBase(BaseModel):
    identifier: str
    content: str


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    identifier: Optional[str] = None
    content: Optional[str] = None


class Document(DocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# DocumentMeta schemas
class DocumentMetaBase(BaseModel):
    document_id: int
    key: str
    value: str


class DocumentMetaCreate(DocumentMetaBase):
    pass


class DocumentMetaUpdate(BaseModel):
    key: Optional[str] = None
    value: Optional[str] = None


class DocumentMeta(DocumentMetaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
