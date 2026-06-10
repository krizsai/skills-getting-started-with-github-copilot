from urllib.parse import quote


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_root_redirect(client):
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code in (307, 302)
    assert resp.headers["location"] == "/static/index.html"


def test_signup_success(client):
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    resp = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    assert resp.status_code == 200
    data = resp.json()
    assert f"Signed up {email} for {activity}" in data["message"]

    # Verify participant added
    resp2 = client.get("/activities")
    participants = resp2.json()[activity]["participants"]
    assert email in participants


def test_signup_activity_not_found(client):
    resp = client.post("/activities/Nonexistent%20Activity/signup?email=test@x.com")
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Activity not found"


def test_duplicate_signup_rejected(client):
    activity = "Chess Club"
    email = "dup@mergington.edu"
    resp1 = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    assert resp1.status_code == 200
    resp2 = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    assert resp2.status_code == 400
    assert resp2.json().get("detail") == "Student is already signed up for this activity"
