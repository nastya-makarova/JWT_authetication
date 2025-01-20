from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class Test00UserRegistration:
    URL_SIGNUP = "/api/register/"

    def test_00_nodata_signup(self, client):
        response = client.post(self.URL_SIGNUP)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f"The endpoint `{self.URL_SIGNUP}` was not found."
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            "The request does not contain the required data."
        )

    def test_00_invalid_data_signup(self, client, django_user_model):
        invalid_data = {"email": "invalid_email", "password": " "}
        users_count = django_user_model.objects.count()

        response = client.post(self.URL_SIGNUP, data=invalid_data)

        assert users_count == django_user_model.objects.count(), (
            f"Check that a POST request to {self.URL_SIGNUP} with invalid"
            "data does not create a new user."
        )

        valid_email = "validemail@yamdb.fake"
        invalid_data = {
            "email": valid_email,
        }
        response = client.post(self.URL_SIGNUP, data=invalid_data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f"If the POST request to {self.URL_SIGNUP} does not include"
            "username data, a 400 status response should be returned."
        )
        assert users_count == django_user_model.objects.count(), (
            f"Check that a POST request to {self.URL_SIGNUP} without"
            "username data does not create a new user."
        )

    def test_00_valid_data_user_signup(self, client, django_user_model):
        valid_data = {
            "email": "valid@example.com",
            "password": "valid_password123",
        }
        response_data = {
            "id": 1,
            "email": "valid@example.com"
        }

        response = client.post(self.URL_SIGNUP, data=valid_data)

        assert response.status_code == HTTPStatus.CREATED, (
            "A POST request with valid data sent to the endpoint"
            "{self.URL_SIGNUP} should return a 200 status response."
        )
        assert response.json() == response_data, (
            "A POST request with valid data sent to the endpoint"
            "{self.URL_SIGNUP} should return a response containing"
            "the username and email of the created user."
        )

        new_user = django_user_model.objects.filter(email=valid_data["email"])
        assert new_user.exists(), (
            "A POST request with valid data sent to the endpoint"
            "{self.URL_SIGNUP} should create a new user."
        )

        new_user.delete()
