# Rest in Pytest (RiP)

---

## Overview

**Rest in Pytest (RiP)** is a Python library designed for REST API testing. It simplifies the process of API testing by leveraging libraries such as `pytest` and `httpx`. Additionally, it offers a fluent interface design, inspired by _Rest Assured_, for constructing and executing HTTP requests, as well as validating responses.

## Features

- Fluent interface for building HTTP requests
- Flexible request configuration (headers, params, data, SSL verification, etc.)
- Comprehensive response assertions
- Integration with pytest for easy test execution and reporting

## Examples

These examples are based on the tests found in `tests\test_rip.py`.

GET request with parameters and expect a specific status code and JSON path in the response.

```python
def test_get_resource(base_url):
    (
        Rip()
        .given()
        .url(base_url)
        .headers({"Content-Type": "application/json"})
        .params({"userId": 1})
        .when()
        .get("/posts")
        .then()
        .expect_status(200)
        .expect_header_content_type("application/json; charset=utf-8")
        .expect_json_path(
            "$..title",
            [
                "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                "qui est esse",
                "ea molestias quasi exercitationem repellat qui ipsa sit aut",
                "eum et est occaecati",
                "nesciunt quas odio",
                "dolorem eum magni eos aperiam quia",
                "magnam facilis autem",
                "dolorem dolore est ipsam",
                "nesciunt iure omnis dolorem tempora et accusantium",
                "optio molestias id quia eum",
            ],
        )
        .expect_json_contains(
            {
                "userId": 1,
                "id": 1,
                "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto",
            }
        )
    )
```

GET request using keyword arguments, providing a different approach to configuring the request.

```python
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
```

---

POST request with JSON data and expect a specific status code and JSON content in the response.

```python
def test_create_resource(base_url):
    (
        Rip()
        .given()
        .url(base_url)
        .headers({"Content-type": "application/json; charset=UTF-8"})
        .content('{"title": "foo", "body": "bar", "userId": 1}')
        .when()
        .post("/posts")
        .then()
        .expect_status(201)
        # Assert reponse in json
        .expect_json({"id": 101, "title": "foo", "body": "bar", "userId": 1})
        # Assert response content in unicode
        .expect_body(
            '{\n  "title": "foo",\n  "body": "bar",\n  "userId": 1,\n  "id": 101\n}'
        )
    )
```

---

PUT request with JSON data to update a resource and expect a specific status code in the response.

```python
def test_update_resource(base_url):
    (
        Rip()
        .given()
        .url(base_url)
        .headers({"Content-type": "application/json; charset=UTF-8"})
        .json({"title": "foo", "body": "bar", "userId": 1})
        .when()
        .put("/posts/1")
        .then()
        .expect_status(200)
    )
```

---

## Getting Started

### Prerequisites

Ensure you have the following prerequisites installed:

- Python 3.11 or higher
- Poetry (for dependency management)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/jayson-panganiban/rest-in-pytest.git
   ```

2. **Install Dependencies**

   ```bash
   cd rest-in-pytest
   poetry install
   ```

3. Create a `.env` file in the root directory and add the following environment variables:

   ```bash
    #Example
    API_BASE_URL=https://jsonplaceholder.typicode.com
    API_VERSION=1.0
    PROJECT_NAME=RIP
   ```

### Running Tests

Execute tests using pytest:

```bash
pytest -vv
```

Execute tests with pytest-xdist:

```bash
pytest -n auto
```

Generate an HTML report:

```
pytest --html=report.html --self-contained-html
```
