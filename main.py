import requests, os
from datetime import datetime

my_headers = {"Authorization": f'Bearer {os.environ["API_TOKEN"]}'}
response = requests.get(
    "https://api.slangapp.com/challenges/v1/activities", headers=my_headers
).json()

user_activities = {}
for activity in response["activities"]:
    if activity["user_id"] not in user_activities:
        user_activities[activity["user_id"]] = []
    user_activities[activity["user_id"]].append(activity)

# order user activities by their first_seen_at
for user_id in user_activities:
    user_activities[user_id] = sorted(
        user_activities[user_id], key=lambda k: k["first_seen_at"]
    )

print(user_activities)

user_sessions = {}
for user_id, activities in user_activities.items():
    user_sessions[user_id] = []
    for activity in activities:
        if not user_sessions[user_id]:
            temp_dict = {
                "ended_at": activity["answered_at"],
                "started_at": activity["first_seen_at"],
                "activity_ids": [activity["id"]],
                "duration_seconds": (
                    datetime.strptime(activity["answered_at"], "%Y-%m-%dT%H:%M:%S%z")
                    - datetime.strptime(
                        activity["first_seen_at"], "%Y-%m-%dT%H:%M:%S%z"
                    )
                ).total_seconds(),
            }
            user_sessions[user_id].append(temp_dict)
