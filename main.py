import requests, os, json
from datetime import datetime

my_headers = {"Authorization": f'Bearer {os.environ["API_TOKEN"]}'}
response = requests.get(
    "https://api.slangapp.com/challenges/v1/activities", headers=my_headers
).json()

user_activities = {}
for activity in response["activities"]:  # O(n)
    if activity["user_id"] not in user_activities:
        user_activities[activity["user_id"]] = []
    user_activities[activity["user_id"]].append(activity)

# order user activities by their first_seen_at
for user_id in user_activities:  # O(n) x O(m log m) = n x m_log_m
    user_activities[user_id] = sorted(
        user_activities[user_id], key=lambda k: k["first_seen_at"]
    )

user_sessions = {}
for user_id, activities in user_activities.items():  # O(n) x O(m) = n x m
    user_sessions[user_id] = []
    for activity in activities:
        if (
            not user_sessions[user_id]
            or (
                datetime.strptime(activity["first_seen_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                - datetime.strptime(
                    user_sessions[user_id][-1]["ended_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
                )
            ).total_seconds()
            > 300
        ):
            temp_dict = {
                "started_at": activity["first_seen_at"],
                "ended_at": activity["answered_at"],
                "activity_ids": [activity["id"]],
                "duration_seconds": (
                    datetime.strptime(activity["answered_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    - datetime.strptime(
                        activity["first_seen_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
                    )
                ).total_seconds(),
            }
            user_sessions[user_id].append(temp_dict)
        else:
            user_sessions[user_id][-1]["ended_at"] = activity["answered_at"]
            user_sessions[user_id][-1]["activity_ids"].append(activity["id"])
            user_sessions[user_id][-1]["duration_seconds"] = (
                datetime.strptime(
                    user_sessions[user_id][-1]["ended_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
                )
                - datetime.strptime(
                    user_sessions[user_id][-1]["started_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
                )
            ).total_seconds()
print(json.dumps(user_sessions))

# complexity: O(n) + O(n x m_log_m) + O(n x m) = O(n x m_log_m), where n is the number of users and m is the number of activities for each user
