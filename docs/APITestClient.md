# APITestClient Documentation

## Overview

The APITestClient is a FastAPI-style testing utility that allows you to test HTTP API endpoints without making real network requests. It's designed specifically for testing the custom HTTP API framework in this project and provides an in-memory simulation of HTTP requests and responses.

## Features

- **FastAPI-style API**: Familiar interface similar to FastAPI's TestClient
- **No Network Overhead**: All testing happens in-memory for fast test execution
- **Full Response Simulation**: Complete HTTP response objects with status codes, headers, and content
- **Seamless Integration**: Works directly with your existing API class and routing system
- **Type-Safe**: Full type annotations for better IDE support and code quality
- **Pytest Compatible**: Designed to work perfectly with pytest test suites

## Installation & Setup

The APITestClient is located in `/app/core/apiTestClient.py` and requires the following dependencies:

```python
from app.core.api import API
from app.core.apiTestClient import APITestClient
```

## API Reference

### APITestClient Class

```python
class APITestClient:
    def __init__(self, api: API)
    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> TestResponse
    def post(self, path: str, json: Optional[Any] = None, params: Optional[Dict[str, Any]] = None) -> TestResponse
```

#### Constructor

```python
client = APITestClient(api)
```

- **api**: An instance of your API class with registered routes

#### GET Requests

```python
response = client.get(path, params=None)
```

- **path**: The endpoint path (e.g., "/hello", "/users")
- **params**: Optional dictionary of query parameters
- **Returns**: TestResponse object

#### POST Requests

```python
response = client.post(path, json=None, params=None)
```

- **path**: The endpoint path
- **json**: Optional JSON data to send in request body
- **params**: Optional dictionary of query parameters
- **Returns**: TestResponse object

### TestResponse Class

```python
class TestResponse:
    status_code: int          # HTTP status code
    content: bytes           # Raw response content
    headers: Dict[str, str]  # Response headers

    def json(self) -> Any           # Parse response as JSON
    @property
    def text(self) -> str           # Get response as text string
    def __repr__(self) -> str       # String representation
```

#### Properties and Methods

- **status_code**: HTTP status code (200, 404, 500, etc.)
- **content**: Raw response content as bytes
- **headers**: Dictionary of response headers
- **json()**: Parse response content as JSON (raises exception if invalid JSON)
- **text**: Response content as a string (property)

## Usage Examples

### Basic Setup

```python
from app.core.api import API
from app.core.apiTestClient import APITestClient

# Create API instance
api = API()

# Register routes
@api.get("/hello")
def hello_handler(args):
    return {"message": "Hello, World!", "args": args}

@api.post("/echo")
def echo_handler(args):
    return {"received": args, "status": "ok"}

# Create test client
client = APITestClient(api)
```

### GET Requests

```python
# Simple GET request
response = client.get("/hello")
assert response.status_code == 200
assert response.json()["message"] == "Hello, World!"

# GET with query parameters
response = client.get("/hello", params={"name": "John", "age": "30"})
data = response.json()
assert data["args"]["name"] == "John"
assert data["args"]["age"] == "30"
```

### POST Requests

```python
# POST with JSON data
test_data = {"user": "alice", "items": [1, 2, 3]}
response = client.post("/echo", json=test_data)
assert response.status_code == 200
assert response.json()["received"] == test_data

# POST without data
response = client.post("/echo")
assert response.json()["received"] == {}
```

### Response Handling

```python
response = client.get("/hello")

# Check status code
assert response.status_code == 200

# Check headers
assert response.headers["content-type"] == "application/json"

# Get response as text
text_content = response.text
assert "Hello" in text_content

# Parse JSON response
data = response.json()
assert isinstance(data, dict)

# Debug representation
print(response)  # <TestResponse [200]>
```

### Error Handling

```python
# 404 Not Found
response = client.get("/nonexistent")
assert response.status_code == 404
assert response.json()["error"] == "not found"

# Handle exceptions in route handlers
@api.get("/error")
def error_handler(args):
    raise ValueError("Something went wrong")

response = client.get("/error")
assert response.status_code == 500
assert "Something went wrong" in response.json()["error"]
```

## Pytest Integration

### Test File Structure

```python
# tests/app/test_api.py
import pytest
from app.core.api import API
from app.core.apiTestClient import APITestClient

@pytest.fixture
def api():
    """Create API instance with test routes."""
    api_instance = API()

    @api_instance.get("/users")
    def users_handler(args):
        return {"users": [], "count": 0}

    return api_instance

@pytest.fixture
def client(api):
    """Create APITestClient instance."""
    return APITestClient(api)

class TestAPI:
    def test_users_endpoint(self, client):
        """Test users endpoint."""
        response = client.get("/users")
        assert response.status_code == 200
        assert response.json()["count"] == 0
```

### Running Tests

```bash
# Run specific test file
uv run python -m pytest tests/app/test_api.py -v

# Run all tests
uv run python -m pytest -v

# Run with coverage
uv run python -m pytest --cov=app tests/
```

## Advanced Examples

### Complex API Testing

```python
# Example: User management API
@api.get("/users")
def list_users(args):
    # Simulate database query with filtering
    users = [
        {"id": 1, "name": "Alice", "role": "admin"},
        {"id": 2, "name": "Bob", "role": "user"},
        {"id": 3, "name": "Charlie", "role": "user"}
    ]

    # Filter by role if provided
    if "role" in args:
        users = [u for u in users if u["role"] == args["role"]]

    return {"users": users, "count": len(users)}

@api.post("/users")
def create_user(args):
    # Validate required fields
    if not args.get("name"):
        raise ValueError("Name is required")

    # Simulate user creation
    new_user = {
        "id": 999,
        "name": args["name"],
        "role": args.get("role", "user")
    }

    return {"user": new_user, "created": True}

# Test the API
def test_user_filtering():
    client = APITestClient(api)

    # Get all users
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json()["count"] == 3

    # Filter by role
    response = client.get("/users", params={"role": "admin"})
    data = response.json()
    assert data["count"] == 1
    assert data["users"][0]["name"] == "Alice"

def test_user_creation():
    client = APITestClient(api)

    # Valid user creation
    user_data = {"name": "David", "role": "moderator"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 200
    result = response.json()
    assert result["created"] is True
    assert result["user"]["name"] == "David"

    # Invalid user creation (missing name)
    response = client.post("/users", json={"role": "user"})
    assert response.status_code == 500
    assert "Name is required" in response.json()["error"]
```

### Testing Real Application Routes

```python
# Test the actual routes from main.py
def test_main_routes():
    from app.core.config import Settings
    from app.main import create_app
    import logging

    # Create the actual app
    settings = Settings()
    logger = logging.getLogger(__name__)
    api = create_app(settings, logger)

    # Test with APITestClient
    client = APITestClient(api)

    # Test index route
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert data["actions"] == ["health"]

    # Test health route
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

## Implementation Details

### How It Works

1. **Route Matching**: The APITestClient accesses the API's `routing` dictionary to find registered routes
2. **Mock Execution**: Routes are called directly with prepared arguments (no HTTP server involved)
3. **Response Simulation**: Results are wrapped in TestResponse objects with proper HTTP semantics
4. **Error Handling**: Exceptions in route handlers are caught and converted to 500 responses

### Architecture

```
APITestClient
    ↓ (calls)
API.routing[method][path]
    ↓ (executes)
Your Route Handler Function
    ↓ (returns)
JSON Result
    ↓ (wraps)
TestResponse Object
```

### Compatibility

- **Python Version**: 3.12+ (uses modern type hints)
- **Dependencies**: Built-in libraries only (no external deps beyond your API framework)
- **Testing Framework**: Designed for pytest but works with any testing framework
- **API Framework**: Compatible with the custom API class in this project

## Best Practices

### 1. Use Fixtures for Setup

```python
@pytest.fixture
def authenticated_client(api):
    """Client with authentication setup."""
    # Add auth routes to API
    @api.post("/login")
    def login(args):
        return {"token": "fake-jwt-token"}

    return APITestClient(api)
```

### 2. Test Both Success and Error Cases

```python
def test_endpoint_validation(client):
    # Test valid input
    response = client.post("/data", json={"valid": "input"})
    assert response.status_code == 200

    # Test invalid input
    response = client.post("/data", json={})
    assert response.status_code == 500
```

### 3. Use Descriptive Test Names

```python
def test_get_users_returns_empty_list_when_no_users_exist(client):
    pass

def test_post_user_creates_user_with_default_role_when_role_not_specified(client):
    pass
```

### 4. Organize Tests by Feature

```python
class TestUserManagement:
    def test_list_users(self, client):
        pass

    def test_create_user(self, client):
        pass

    def test_update_user(self, client):
        pass

class TestAuthentication:
    def test_login(self, client):
        pass

    def test_logout(self, client):
        pass
```

## Troubleshooting

### Common Issues

1. **ImportError**: Ensure all dependencies are installed and paths are correct
2. **Route Not Found**: Check that routes are registered before creating APITestClient
3. **JSON Parse Error**: Verify that route handlers return JSON-serializable data
4. **Type Errors**: Ensure proper type annotations match expected data types

### Debug Tips

```python
# Debug response content
response = client.get("/endpoint")
print(f"Status: {response.status_code}")
print(f"Headers: {response.headers}")
print(f"Content: {response.text}")

# Debug API routing
print(f"Available routes: {api.routing}")
```

## Performance

- **Speed**: Tests run in microseconds (no network latency)
- **Memory**: Minimal overhead (no server process)
- **Scalability**: Can handle thousands of test requests per second
- **Isolation**: Each APITestClient instance is independent

## Comparison with Alternatives

| Feature | APITestClient | Real HTTP Server | Mock Responses |
|---------|------------|------------------|----------------|
| Speed | ⚡ Fastest | 🐌 Slow | ⚡ Fast |
| Realism | 🎯 High | 💯 Perfect | ❌ Low |
| Setup | ✅ Simple | 🔧 Complex | ✅ Simple |
| Debugging | ✅ Easy | 🔧 Harder | ✅ Easy |
| Dependencies | ✅ None | 🏗️ Server setup | ✅ Minimal |

The APITestClient provides the perfect balance of speed, realism, and simplicity for testing HTTP APIs.

---

*This APITestClient implementation was created specifically for the custom HTTP API framework in this project and provides FastAPI-style testing capabilities without external dependencies.*