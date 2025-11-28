import requests
import time
import random

url = "https://l00188491-web-app-pipeline-h0breuchbbf3hvfm.swedencentral-01.azurewebsites.net"
categories = ['motivational', 'wisdom', 'humor']

for i in range(50):
    # Mix of random quotes and category quotes
    if random.choice([True, False]):
        requests.get(f"{url}/api/quote")
    else:
        cat = random.choice(categories)
        requests.get(f"{url}/api/quote/category/{cat}")
    
    time.sleep(0.5)  # Half second between requests
    print(f"Request {i+1} sent")