def test_upload_and_resize(client):
    with open("data/book1.csv", "rb") as file:
        response = client.post("/upload/", files={"file": file})
        response_json = response.json()
        file_id = response_json["file_id"]
    assert response.status_code == 200
    assert response.json() == {"status":"Images uploaded and resized successfully.","file_id":file_id}

