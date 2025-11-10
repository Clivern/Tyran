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
from app.core.config import configs
from app.core.logger import get_logger
from app.db.client import engine, wait_for_db
from app.db.scheme import Base
from app.service.qdrant import get_qdrant


def _migrate_database() -> None:
    logger = get_logger()
    logger.info("Attempt to migrate the database")
    wait_for_db(engine, 30)
    Base.metadata.create_all(bind=engine)
    logger.info("Database is migrated")


def _ensure_vector_collection() -> None:
    if configs.vector_search_driver.lower() != "qdrant":
        return

    logger = get_logger()
    logger.info(f"Ensure Qdrant collection {configs.qdrant_db_collection} exists")
    qdrant_client = get_qdrant()
    qdrant_client.create_collection_if_not_exist(configs.qdrant_db_collection)
    qdrant_client.ensure_payload_index(
        configs.qdrant_db_collection, configs.qdrant_db_index
    )
    logger.info(f"Qdrant collection {configs.qdrant_db_collection} is ready")


def run_initial_migrations() -> None:
    _migrate_database()
    _ensure_vector_collection()
