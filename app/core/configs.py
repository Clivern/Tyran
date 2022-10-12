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

import os
import os.path
from app import APP_ROOT
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


if os.path.exists(os.path.join(APP_ROOT, ".env")):
    load_dotenv(dotenv_path=os.path.join(APP_ROOT, ".env"))
else:
    load_dotenv(dotenv_path=os.path.join(APP_ROOT, ".env.example"))


class Configs(BaseSettings):

    app_name: str = "Tyran"
    app_description: str = "A Vector Search as a Service"
    app_key: str = ")lj2@3@y&5ofgoekbt2c-4$$w2bedn@-(hr&i^!#%wype&wp6d"
    app_debug_mode: bool = False
    app_url: str = "https://tyran.sh"
    app_email: str = "hello@clivern.com"

    db_connection: str = "sqlite"
    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_database: str = "storage/db/tyran"
    db_username: str = "root"
    db_password: str = "root"

    vector_search_driver: str = "qdrant"
    openai_api_key: str = ""

    chroma_db_collection: str = "tyrcollect"

    qdrant_db_url: str = ""
    qdrant_db_api_key: str = ""
    qdrant_db_collection: str = "tyrcollect"

    app_logging_handlers: str = "console"
    app_logging_level: str = "info"

    allowed_hosts: str = "*"
    app_timezone: str = "UTC"
    app_language: str = "en-us"

    def get_db_connection(self):
        if self.db_connection.lower() == "sqlite":
            return f"sqlite:///{self.db_database}.db"  # noqa: E231
        else:
            return f"{self.db_connection}://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_database}"


configs = Configs()
