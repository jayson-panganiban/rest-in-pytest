import pytest

from rest_in_pytest import Rip


# GET test
# Filtering a resource using query params
def test_get_resource(base_url):
    (
        Rip()
        .given()
        .base_url(base_url)
        .headers({'Content-Type': 'application/json'})
        .params({'userId': 1})
        .when()
        .get('/posts')
        .then()
        .expect_status(200)
        .expect_header_content_type('application/json; charset=utf-8')
        .expect_json_path('$.userId', 'userId')
        .expect_json_contains(
            {
                'userId': 1,
                'id': 1,
                'title': 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit',
                'body': 'quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto',
            }
        )
    )


# Using keyword args in GET
def test_get_params(base_url):
    (
        Rip()
        .given(base_url)
        .when()
        .get(
            endpoint='/posts',
            headers={'Content-Type': 'application/json'},
            params={'userId': 1},
        )
        .then()
        .expect_status(200)
    )


# POST test
def test_create_resource(base_url):
    (
        Rip()
        .given()
        .base_url(base_url)
        .data('{"title": "foo", "body": "bar", "userId": 1}')
        .headers({'Content-type': 'application/json; charset=UTF-8'})
        .when()
        .post('/posts')
        .then()
        .expect_status(201)
        # Assert reponse in json
        .expect_json({'id': 101, 'title': 'foo', 'body': 'bar', 'userId': 1})
        # Assert response content in unicode
        .expect_body(
            '{\n  "title": "foo",\n  "body": "bar",\n  "userId": 1,\n  "id": 101\n}'
        )
    )


# Using keyword args in POST
def test_post_params(base_url):
    (
        Rip()
        .given(base_url)
        .when()
        .post(
            endpoint='/posts',
            data='{"title": "foo", "body": "bar", "userId": 1}',
            headers={'Content-type': 'application/json; charset=UTF-8'},
        )
        .then()
        .expect_status(201)
    )


# PUT test
def test_update_resource(base_url):
    (
        Rip()
        .given()
        .base_url(base_url)
        .json_data({'title': 'foo', 'body': 'bar', 'userId': 1})
        .headers({'Content-type': 'application/json; charset=UTF-8'})
        .when()
        .put('/posts/1')
        .then()
        .expect_status(200)
    )


# PATCH test
def test_patch_resource(base_url):
    (
        Rip()
        .given()
        .base_url(base_url)
        .json_data({'title': 'foo'})
        .headers({'Content-type': 'application/json; charset=UTF-8'})
        .when()
        .patch('/posts/1')
        .then()
        .expect_status(200)
    )


# DELETE test
def test_delete_resource(base_url):
    (
        Rip()
        .given()
        .base_url(base_url)
        .ssl_verify()
        .when()
        .delete('/posts/1')
        .then()
        .expect_status(200)
    )


# TODO: Add test for other HTTP methods
# def test_patch(base_url): NotImplemented
# def test_head(base_url): NotImplemented
# def test_options(base_url): NotImplemented
# def test_trace(base_url): NotImplemented
# def test_connect(base_url): NotImplemented


@pytest.mark.parametrize(
    'path_params',
    [
        1,
        2,
    ],
)
def test_specs(base_url, path_params):
    (
        Rip()
        .given()
        .base_url(base_url)
        .params()
        .data()
        .headers()
        .cookies()
        .files()
        .auth()
        # TODO: NotImplemented
        # .timeout()
        # .allow_redirects()
        # .hooks()
        .proxies()
        .stream()
        .ssl_verify()
        .cert()
        .json_data()
        .when()
        .get(endpoint=f'/posts/{path_params}')
        .then()
        .expect_status(200)
    )


# TODO: Cover other scenarios
# TODO: Add other expectations (expect_json_schema, etc)
