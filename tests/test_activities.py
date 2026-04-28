def test_get_activities_returns_success(client):
    response = client.get("/activities")

    assert response.status_code == 200


def test_get_activities_has_expected_shape(client):
    response = client.get("/activities")
    data = response.json()

    assert isinstance(data, dict)
    assert "Chess Club" in data

    chess = data["Chess Club"]
    assert "description" in chess
    assert "schedule" in chess
    assert "max_participants" in chess
    assert "participants" in chess
    assert isinstance(chess["participants"], list)
