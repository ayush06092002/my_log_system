import requests
import json
from faker import Faker
import time

url = 'http://127.0.0.1:3000/ingest'
fake = Faker()

while True:
    log_entry = {
        "level": fake.random_element(elements=('info', 'warning', 'error')),
        "message": fake.sentence(),
        "resourceId": fake.uuid4(),
        "timestamp": fake.iso8601(),
        "traceId": fake.uuid4(),
        "spanId": fake.uuid4(),
        "commit": fake.sha1(),
        "metadata": {
            "parentResourceId": fake.uuid4()
        }
    }

    response = requests.post(url, json=log_entry)
    print(response.status_code)
    time.sleep(3)  # Adjust the delay based on your requirements
