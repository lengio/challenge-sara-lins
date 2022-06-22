import requests, os
from datetime import datetime


def iso_string_to_datetime(time):
    """Transform from ISO to datetime"""
    return datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f%z")


def diff_to_sec(time1, time2):
    """Transform the difference between two times to seconds"""
    time = iso_string_to_datetime(time1) - iso_string_to_datetime(time2)

    return time.total_seconds()


def group_activities_by_user(data):
    """Group all activities by user and order by first_seen_at"""
    user_activities = {}
    for activity in data["activities"]:  # O(n)
        if activity["user_id"] not in user_activities:
            user_activities[activity["user_id"]] = []
        user_activities[activity["user_id"]].append(activity)

    # order user activities by their first_seen_at
    for user_id in user_activities:  # O(n) x O(m log m) = O(n x m_log_m)
        user_activities[user_id] = sorted(
            user_activities[user_id], key=lambda k: k["first_seen_at"]
        )

    return user_activities


def create_user_sessions(activities_by_user):
    """Create a dict with user_id as key and a list of sessions as value"""
    user_sessions = {}
    for user_id, activities in activities_by_user.items():  # O(n) x O(m) = O(n x m)
        user_sessions[user_id] = []
        for activity in activities:
            if (
                not user_sessions[user_id]
                or (
                    diff_to_sec(
                        activity["first_seen_at"],
                        user_sessions[user_id][-1]["ended_at"],
                    )
                )
                > 300
            ):
                temp_dict = {
                    "started_at": activity["first_seen_at"],
                    "ended_at": activity["answered_at"],
                    "activity_ids": [activity["id"]],
                    "duration_seconds": diff_to_sec(
                        activity["answered_at"], activity["first_seen_at"]
                    ),
                }
                user_sessions[user_id].append(temp_dict)
            else:
                user_sessions[user_id][-1]["ended_at"] = activity["answered_at"]
                user_sessions[user_id][-1]["activity_ids"].append(activity["id"])
                user_sessions[user_id][-1]["duration_seconds"] = diff_to_sec(
                    user_sessions[user_id][-1]["ended_at"],
                    user_sessions[user_id][-1]["started_at"],
                )
    return {"user_sessions": user_sessions}


def api_get(my_headers):
    """Get activities from the API"""
    req = requests.get(
        "https://api.slangapp.com/challenges/v1/activities", headers=my_headers
    )
    if req.status_code == 200:
        print("Successfully got activities from the API")
        return req.json()
    else:
        print("An error ocurred. Status Code: ", req.status_code)
        req.raise_for_status()


def api_post(user_sessions, my_headers):
    """Post user_sessions to the API"""
    req = requests.post(
        "https://api.slangapp.com/challenges/v1/activities/sessions",
        headers=my_headers,
        json=user_sessions,
        timeout=5,
    )
    if req.status_code == 204:
        print("Successfully posted user_sessions to the API")
    else:
        print("An error ocurred. Status Code: ", req.status_code)
        req.raise_for_status()


if __name__ == "__main__":
    my_headers = {"Authorization": f'Bearer {os.environ["API_TOKEN"]}'}

    initial_data = api_get(my_headers)
    user_activities = group_activities_by_user(initial_data)
    user_sessions = create_user_sessions(user_activities)
    api_post(user_sessions, my_headers)
    print("\nEnd of program")
