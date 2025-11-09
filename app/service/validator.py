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

import json

from jsonschema import validate
from jsonschema import ValidationError

from app import APP_ROOT
from app.core.logger import Logger


class Validator:
    def __init__(self):
        self.logger = Logger().get_logger(__name__)

    def validate(self, data, schema_path):
        self.error = ""

        f = open(schema_path, "r")
        schema = json.loads(f.read())

        if not isinstance(data, dict):
            try:
                data = json.loads(data)
            except Exception:
                self.error = "Invalid request data"
                return False

        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            error_field = ""
            if "id" in e.schema.keys():
                error_field = "Invalid field {}: ".format(e.schema["id"])
            self.error = error_field + str(e.message)

            return False

        return True

    def get_schema_path(self, rel_path):
        return "{root}{rel_path}".format(root=APP_ROOT, rel_path=rel_path)

    def get_error(self):
        return self.error


def get_validator() -> Validator:
    return Validator()
