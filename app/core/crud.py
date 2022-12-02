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

from sqlalchemy.orm import Session
from app.core import models, schemas


# Option CRUD operations
def create_option(db: Session, option: schemas.OptionCreate):
    db_option = models.Option(**option.dict())
    db.add(db_option)
    db.commit()
    db.refresh(db_option)
    return db_option


def get_option(db: Session, option_id: int):
    return db.query(models.Option).filter(models.Option.id == option_id).first()


def get_option_by_key(db: Session, key: str):
    return db.query(models.Option).filter(models.Option.key == key).first()


def get_options(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Option).offset(skip).limit(limit).all()


def update_option(db: Session, option_id: int, option: schemas.OptionUpdate):
    db_option = db.query(models.Option).filter(models.Option.id == option_id).first()
    if db_option:
        for key, value in option.dict(exclude_unset=True).items():
            setattr(db_option, key, value)
        db.commit()
        db.refresh(db_option)
    return db_option


def delete_option(db: Session, option_id: int):
    db_option = db.query(models.Option).filter(models.Option.id == option_id).first()
    if db_option:
        db.delete(db_option)
        db.commit()
    return db_option


# Document CRUD operations
def create_document(db: Session, document: schemas.DocumentCreate):
    db_document = models.Document(**document.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def get_document(db: Session, document_id: int):
    return db.query(models.Document).filter(models.Document.id == document_id).first()


def get_document_by_identifier(db: Session, identifier: str):
    return (
        db.query(models.Document)
        .filter(models.Document.identifier == identifier)
        .first()
    )


def get_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Document).offset(skip).limit(limit).all()


def get_documents_by_identifiers(db: Session, identifiers: list):
    return (
        db.query(models.Document)
        .filter(models.Document.identifier.in_(identifiers))
        .all()
    )


def update_document(db: Session, document_id: int, document: schemas.DocumentUpdate):
    db_document = (
        db.query(models.Document).filter(models.Document.id == document_id).first()
    )
    if db_document:
        for key, value in document.dict(exclude_unset=True).items():
            setattr(db_document, key, value)
        db.commit()
        db.refresh(db_document)
    return db_document


def delete_document(db: Session, document_id: int):
    db_document = (
        db.query(models.Document).filter(models.Document.id == document_id).first()
    )
    if db_document:
        db.delete(db_document)
        db.commit()
    return db_document


# DocumentMeta CRUD operations
def create_document_meta(db: Session, meta: schemas.DocumentMetaCreate):
    db_meta = models.DocumentMeta(**meta.dict())
    db.add(db_meta)
    db.commit()
    db.refresh(db_meta)
    return db_meta


def get_document_meta(db: Session, meta_id: int):
    return (
        db.query(models.DocumentMeta).filter(models.DocumentMeta.id == meta_id).first()
    )


def get_document_meta_by_document(db: Session, document_id: int):
    return (
        db.query(models.DocumentMeta)
        .filter(models.DocumentMeta.document_id == document_id)
        .all()
    )


def update_document_meta(db: Session, meta_id: int, meta: schemas.DocumentMetaUpdate):
    db_meta = (
        db.query(models.DocumentMeta).filter(models.DocumentMeta.id == meta_id).first()
    )
    if db_meta:
        for key, value in meta.dict(exclude_unset=True).items():
            setattr(db_meta, key, value)
        db.commit()
        db.refresh(db_meta)
    return db_meta


def delete_document_meta(db: Session, meta_id: int):
    db_meta = (
        db.query(models.DocumentMeta).filter(models.DocumentMeta.id == meta_id).first()
    )
    if db_meta:
        db.delete(db_meta)
        db.commit()
    return db_meta


def delete_document_metas_by_document_id(db: Session, document_id: int):
    db_metas = (
        db.query(models.DocumentMeta)
        .filter(models.DocumentMeta.document_id == document_id)
        .all()
    )

    for db_meta in db_metas:
        db.delete(db_meta)

    db.commit()
    return db_metas
