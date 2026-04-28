from src.app import activities

CHESS_SIGNUP_PATH = "/activities/Chess%20Club/signup"


def test_unregister_removes_existing_participant(client):
    email = "michael@mergington.edu"

    response = client.delete(CHESS_SIGNUP_PATH, params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"

    activity_data = client.get("/activities").json()
    assert email not in activity_data["Chess Club"]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete("/activities/Unknown%20Club/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_when_student_not_signed_up(client):
    response = client.delete(CHESS_SIGNUP_PATH, params={"email": "not-enrolled@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_removes_all_duplicates_for_same_email(client):
    duplicate_email = "dupe@mergington.edu"
    activities["Chess Club"]["participants"].extend([duplicate_email, duplicate_email])

    response = client.delete(CHESS_SIGNUP_PATH, params={"email": duplicate_email})

    assert response.status_code == 200

    remaining_participants = client.get("/activities").json()["Chess Club"]["participants"]
    assert duplicate_email not in remaining_participants
