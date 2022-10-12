import requests

# Specify the API endpoint URL
url = 'http://127.0.0.1:8000/api/v1/document'

# Set the headers
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

# Loop through the files
for i in range(1, 15):
    filename = f'testdata/runbook{i}.md'

    # Read the file content
    with open(filename, 'r') as file:
        content = file.read()

    # Prepare the request data
    data = {
        "content": content,
        "metadata": {
            "type": "runbook",
            "team": "devops"
        }
    }

    # Send the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check the response status code
    if response.status_code == 200:
        print(f"Successfully uploaded {filename}")
    else:
        print(f"Failed to upload {filename}")
        print(response.text)
