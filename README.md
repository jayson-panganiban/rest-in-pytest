# rest-in-pytest
---
## Overview
**`rest-in-pytest`** is designed to facilitate the testing of REST APIs. It uses a Fluent Interface and a Gherkin-inspired DSL for easy configuration of HTTP requests and response expectations. 

### Features
- **Domain-Specific Language (DSL)**: Makes test scenarios easy to write and understand with a fluent interface.
- **Configuration**:  Offers a mechanism to build request configurations such as base URL, parameters, data, headers, cookies, files, SSL verification, and more, providing a comprehensive setup for HTTP requests.
- **Expectations**: Provides a mechanism for setting expectations on the HTTP response, including status codes, headers, cookies, body content, and JSON schema validation.
- **Integration with pytest and requests**: Leverages `pytest` and `requests` HTTP modules.
---
## Examples
These examples are based on the tests found in `test_rip.py`. Base url is configured in `conftest.py`.

GET request with parameters and expect a specific status code and JSON path in the response.
```python
# test_rip.py

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
        .base_url(base_url)
        .data('{"title": "foo", "body": "bar", "userId": 1}')
        .headers({'Content-type': 'application/json; charset=UTF-8'})
        .when()
        .post('/posts')
        .then()
        .expect_status(201)
        .expect_json({'id': 101, 'title': 'foo', 'body': 'bar', 'userId': 1})
        .expect_body(
            '{\n "title": "foo",\n "body": "bar",\n "userId": 1,\n "id": 101\n}'
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
        .base_url(base_url)
        .json_data({'title': 'foo', 'body': 'bar', 'userId': 1})
        .headers({'Content-type': 'application/json; charset=UTF-8'})
        .when()
        .put('/posts/1')
        .then()
        .expect_status(200)
    )
```
---
## Getting Started

### Prerequisites
Ensure you have the following prerequisites installed:

- Python 3.11 or higher

### Installation
1. **Clone the Repository**

   First, clone the repository to your local machine:

   ```bash
   git clone <repository-url>
   ```
   
2. **Set Up a Virtual Environment**

   It's recommended to use a virtual environment for Python projects. This helps to keep dependencies required by different projects separate. Create a virtual environment using the following command:

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:

   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```

   - On Unix or MacOS:
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**

   Navigate to the project directory and install the project dependencies using Poetry:

   ```bash
   cd rest-in-pytest
   poetry install
   ```
   This command installs all the dependencies listed in the `pyproject.toml` file.

### Testing
This project uses `pytest` for testing. To run the tests, execute the following command in the project's root directory:

```bash
pytest
```