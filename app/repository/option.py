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

from sqlalchemy.orm import Session

from app.db import scheme
from app.model import Option, OptionCreate


class OptionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, option: OptionCreate) -> Option:
        db_option = scheme.Option(**option.model_dump())
        self._session.add(db_option)
        self._session.commit()
        self._session.refresh(db_option)
        return Option.model_validate(db_option)

    def get(self, option_id: int) -> Optional[Option]:
        db_option = (
            self._session.query(scheme.Option)
            .filter(scheme.Option.id == option_id)
            .first()
        )
        return Option.model_validate(db_option) if db_option else None

    def get_by_key(self, key: str) -> Optional[Option]:
        db_option = (
            self._session.query(scheme.Option).filter(scheme.Option.key == key).first()
        )
        return Option.model_validate(db_option) if db_option else None

    def delete(self, option_id: int) -> Optional[Option]:
        db_option = (
            self._session.query(scheme.Option)
            .filter(scheme.Option.id == option_id)
            .first()
        )
        if db_option is None:
            return None
        self._session.delete(db_option)
        self._session.commit()
        return Option.model_validate(db_option)
