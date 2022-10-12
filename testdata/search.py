import argparse
import requests
import json

def main(search_text):
    # Specify the API endpoint URL
    url = 'http://127.0.0.1:8000/api/v1/document/search'

    # Set the headers
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Prepare the request data
    data = {
        "text": search_text,
        "limit": 3,
        "metadata": {
            "type": "runbook",
            "team": "devops"
        }
    }

    # Send the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check the response status code
    if response.status_code == 200:
        print("Response from server:")
        print(json.dumps(response.json(), indent=2))  # Pretty print the JSON response
    else:
        print(f"Failed to perform search. Status code: {response.status_code}")
        print("Response text:", response.text)

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Search documents using the API.')
    parser.add_argument('text', type=str, help='The text to search for in the documents.')

    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with the provided search text
    main(args.text)
