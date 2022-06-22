import requests, os
from datetime import datetime

my_headers = {"Authorization": f'Bearer {os.environ["API_TOKEN"]}'}


def api_get():
    """Get activities from the API"""
    try:
        return requests.get(
            "https://api.slangapp.com/challenges/v1/activities", headers=my_headers
        ).json()
    except Exception as e:
        print("An error ocurred: ", e)
        return None


def activities_by_user():
    """Group all activities by user and order by first_seen_at"""
    user_activities = {}
    for activity in api_get()["activities"]:  # O(n)
        if activity["user_id"] not in user_activities:
            user_activities[activity["user_id"]] = []
        user_activities[activity["user_id"]].append(activity)

    # order user activities by their first_seen_at
    for user_id in user_activities:  # O(n) x O(m log m) = O(n x m_log_m)
        user_activities[user_id] = sorted(
            user_activities[user_id], key=lambda k: k["first_seen_at"]
        )

    return user_activities


def transform_time(time):
    """Transform time to a readable format"""
    return datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f%z")


user_sessions = {"user_sessions": {}}
for user_id, activities in activities_by_user().items():  # O(n) x O(m) = O(n x m)
    user_sessions["user_sessions"][user_id] = []
    for activity in activities:
        if (
            not user_sessions["user_sessions"][user_id]
            or (
                transform_time(activity["first_seen_at"])
                - transform_time(
                    user_sessions["user_sessions"][user_id][-1]["ended_at"]
                )
            ).total_seconds()
            > 300
        ):
            temp_dict = {
                "started_at": activity["first_seen_at"],
                "ended_at": activity["answered_at"],
                "activity_ids": [activity["id"]],
                "duration_seconds": (
                    transform_time(activity["answered_at"])
                    - transform_time(activity["first_seen_at"])
                ).total_seconds(),
            }
            user_sessions["user_sessions"][user_id].append(temp_dict)
        else:
            user_sessions["user_sessions"][user_id][-1]["ended_at"] = activity[
                "answered_at"
            ]
            user_sessions["user_sessions"][user_id][-1]["activity_ids"].append(
                activity["id"]
            )
            user_sessions["user_sessions"][user_id][-1]["duration_seconds"] = (
                transform_time(user_sessions["user_sessions"][user_id][-1]["ended_at"])
                - transform_time(
                    user_sessions["user_sessions"][user_id][-1]["started_at"]
                )
            ).total_seconds()

# complexity: O(n) + O(n x m_log_m) + O(n x m) = O(n x m_log_m), where n is the number of users and m is the number of activities for each user

requests.post(
    "https://api.slangapp.com/challenges/v1/activities/sessions",
    headers=my_headers,
    json=user_sessions,
    timeout=5,
)
