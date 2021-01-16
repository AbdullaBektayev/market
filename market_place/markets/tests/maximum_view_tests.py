# import pytest
import requests
# @pytest.mark.django_db
def test_view(client):
    response = requests.get("http://0.0.0.0:8000/api/v1/category/maxprice/")
    response_body = response.json()
    assert response_body[0]["price"] == 777777
    assert response_body[1]["price"] == 1799900
    assert response_body[2]["price"] == 2807990
    assert response_body[3]["price"] == 959900
