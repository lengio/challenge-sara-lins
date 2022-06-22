import requests
import os

my_headers = {'Authorization' : f'Bearer {os.environ["API_TOKEN"]}'}
response = requests.get('https://api.slangapp.com/challenges/v1/activities', headers=my_headers).json()

user_activities = {}
for activity in response['activities']:
  if activity['user_id'] not in user_activities:
    user_activities[activity['user_id']] = []
  user_activities[activity['user_id']].append(activity)
  
# order user activities by their first_seen_at
for user_id in user_activities:
  user_activities[user_id] = sorted(user_activities[user_id], key=lambda k: k['first_seen_at'])

print(user_activities)
