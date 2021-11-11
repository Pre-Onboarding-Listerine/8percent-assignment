from assertpy import assert_that


def test_signup_with_valid_info(test_client):
    data = {
        "name": "asd",
        "password": "123qwe"
    }
    response = test_client.post(
        "/api/users",
        json=data
    )

    assert_that(response.status_code).is_equal_to(201)
