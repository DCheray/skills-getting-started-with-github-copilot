CHESS_SIGNUP_PATH = "/activities/Chess%20Club/signup"


def test_signup_successfully_registers_student(client):
    email = "newstudent@mergington.edu"

    response = client.post(CHESS_SIGNUP_PATH, params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post("/activities/Unknown%20Club/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_duplicate_registration(client):
    existing_email = "michael@mergington.edu"

    response = client.post(CHESS_SIGNUP_PATH, params={"email": existing_email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
