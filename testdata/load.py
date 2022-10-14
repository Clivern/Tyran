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

from pytyran.client import Client
from pytyran.reader import Reader


reader = Reader()
tyran_client = Client("http://127.0.0.1:8000")

# Loop through the files
for i in range(1, 15):
    filename = f"testdata/runbook{i}.md"

    # Read the file content
    content = reader.read_file(filename)

    # Send the POST request
    response = tyran_client.create_document(
        content, {"type": "runbook", "team": "devops"}
    )

    # Check the response status code
    if response.status_code == 200:
        print(f"Successfully uploaded {filename}")
    else:
        print(f"Failed to upload {filename}")
        print(response.text)
