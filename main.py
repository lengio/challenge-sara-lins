import requests
import os

my_headers = {'Authorization' : f'Bearer {os.environ["API_TOKEN"]}'}
response = requests.get('https://api.slangapp.com/challenges/v1/activities', headers=my_headers).json()

print(response)