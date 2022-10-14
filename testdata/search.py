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

import argparse
import json
from pytyran.client import Client


def main(search_text):
    tyran_client = Client("http://127.0.0.1:8000")

    # Send the POST request
    response = tyran_client.search_documents(
        search_text, {"type": "runbook", "team": "devops"}, 3
    )

    # Check the response status code
    if response.status_code == 200:
        print("Response from server:")
        # Pretty print the JSON response
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Failed to perform search. Status code: {response.status_code}")
        print("Response text:", response.text)


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Search documents using the API.")
    parser.add_argument(
        "text", type=str, help="The text to search for in the documents."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with the provided search text
    main(args.text)
