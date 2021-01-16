import requests


def test_view(client):
    response = requests.get("http://0.0.0.0:8000/api/v1/category/minprice/")
    response_body = response.json()
    assert response_body[0]["price"] == 32900
    assert response_body[1]["price"] == 169990
    assert response_body[2]["price"] == 128990
    assert response_body[3]["price"] == 22290
