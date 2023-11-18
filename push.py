import requests
import json

# Replace with the actual URL of your Flask app
url = 'http://127.0.0.1:3000/ingest'

# Read log data from a file
with open('log_data.json', 'r') as file:
    log_entries = json.load(file)

# Send the POST request with the log entries from the file
response = requests.post(url, json=log_entries)

# Print the response
print(response.status_code)
print(response.json())
