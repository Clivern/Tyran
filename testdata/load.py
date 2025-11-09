# MIT License
#
# Copyright (c) 2024 Clivern
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

from pathlib import Path

import requests


BASE_URL = "http://127.0.0.1:8000/api/v1/document"
TIMEOUT = 10
CATEGORY = "runbook"
TESTDATA_DIR = Path(__file__).resolve().parent


# Loop through the files
for i in range(1, 15):
    filename = TESTDATA_DIR / f"runbook{i}.md"

    # Read the file content
    content = filename.read_text(encoding="utf-8")

    try:
        response = requests.post(
            BASE_URL,
            json={"content": content, "category": CATEGORY},
            timeout=TIMEOUT,
        )
    except requests.RequestException as exc:
        print(f"Failed to upload {filename}: {exc}")
        continue

    # Check the response status code
    if response.status_code == 201:
        print(f"Successfully uploaded {filename}")
    else:
        print(f"Failed to upload {filename}: {response.status_code}")
        print(response.text)
