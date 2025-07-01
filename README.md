# Mini IAM API with Flask & JWT

A Flask-based REST API demonstrating JWT authentication and role-based access control (RBAC) for learning purposes.

## Features

- User registration and authentication
- JWT token-based authentication
- Role-based access control (RBAC)
- Protected endpoints with different permission levels
- Admin panel functionality

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- PyJWT
- Werkzeug

### Installation

1. Clone the repository
2. Install dependencies
3. Set your SECRET_KEY environment variable
4. Run the Flask application

```bash
python app.py
```

## API Endpoints

### 1. Register a New User

**Endpoint:** `POST /register`

**Request Body:**
```json
{
    "username": "newuser",
    "password": "strongpassword"
}
```

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"username": "newuser", "password": "strongpassword"}' \
     http://127.0.0.1:5000/register
```

**Response:**
```json
{
    "message": "User registered successfully", 
    "username": "newuser"
}
```

### 2. Login User to Get JWT

**Endpoint:** `POST /login`

**Request Body:**
```json
{
    "username": "newuser",
    "password": "strongpassword"
}
```

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"username": "newuser", "password": "strongpassword"}' \
     http://127.0.0.1:5000/login
```

**Response:**
```json
{
    "message": "Login successful", 
    "token": "your_jwt_token_here"
}
```

> **Important:** Copy the token value from this response. You will use it for all subsequent authenticated requests.

### 3. Access Protected User Data

**Endpoint:** `GET /api/user_data`

**Headers:** `Authorization: Bearer <YOUR_JWT_TOKEN>`

**Example:**
```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
     http://127.0.0.1:5000/api/user_data
```

**Response:**
```json
{
    "data": {
        "item1": "value1",
        "item2": "value2"
    },
    "message": "Welcome, newuser! This is your personal data.",
    "your_roles": ["user"]
}
```

### 4. Access Protected Admin Panel

**Endpoint:** `GET /api/admin_panel`

**Headers:** `Authorization: Bearer <YOUR_JWT_TOKEN>`

**Requires:** `admin` role

#### Testing with Regular User (Expected to Fail)
```bash
curl -H "Authorization: Bearer YOUR_NEWUSER_TOKEN_HERE" \
     http://127.0.0.1:5000/api/admin_panel
```

**Response:**
```json
{
    "message": "Access denied: Insufficient permissions."
}
```
*Status: 403 Forbidden*

#### Testing with Admin User
First, login as admin (username: `admin`, password: `adminpassword`) to get the admin JWT, then:

```bash
curl -H "Authorization: Bearer YOUR_ADMIN_TOKEN_HERE" \
     http://127.0.0.1:5000/api/admin_panel
```

**Response:**
```json
{
    "admin_secrets": [
        "secret_key_1",
        "secret_key_2"
    ],
    "message": "Hello, Admin admin! This is the admin panel.",
    "your_roles": [
        "user",
        "admin"
    ]
}
```

### 5. List All Users

**Endpoint:** `GET /api/all_users`

**Headers:** `Authorization: Bearer <YOUR_ADMIN_TOKEN>`

**Requires:** `admin` role

**Example:**
```bash
curl -H "Authorization: Bearer YOUR_ADMIN_TOKEN_HERE" \
     http://127.0.0.1:5000/api/all_users
```

**Response:**
```json
{
    "users": [
        {
            "username": "admin",
            "roles": ["user", "admin"]
        },
        {
            "username": "newuser",
            "roles": ["user"]
        }
    ]
}
```

## IAM Concepts Demonstrated

- **Identity:** User accounts stored in users.json
- **Authentication:** The `/login` endpoint verifies credentials and issues a JWT
- **Authorization:** The `@token_required` and `@roles_required` decorators verify the JWT and check user roles before allowing access to routes
- **Role-Based Access Control (RBAC):** Users are assigned roles (`user`, `admin`), and endpoints are protected based on these roles, providing granular access control
- **Statelessness with JWT:** Once issued, the JWT contains all necessary information (like roles) for authorization checks without needing to query the "database" again until the token expires or is invalidated

## Security Considerations

> **Important:** This is a learning project. Do not use in production without implementing proper security measures.

### Known Limitations

- **SECRET_KEY:** Never hardcode your SECRET_KEY in production. Always load it from environment variables
- **Database:** This project uses a simple JSON file for user data. This is NOT suitable for production. Real-world applications require robust databases (SQL or NoSQL) for scalability, security, and integrity
- **Password Hashing:** While `werkzeug.security` is used for hashing passwords, ensure you understand the importance of secure hashing algorithms and salting
- **JWT Security:** JWTs are signed, not encrypted by default. Sensitive data should not be placed directly in the JWT payload if it needs to remain confidential
- **No Logout/Token Revocation:** This project does not implement JWT revocation (e.g., blacklisting tokens). In a real application, you'd need a mechanism to invalidate tokens (e.g., for logout, password change, or compromise)
- **Error Handling:** The error handling is basic. A production API would have more comprehensive error responses and logging
- **Rate Limiting:** No rate limiting is implemented, which could leave the login endpoint vulnerable to brute-force attacks

## Contributing

Feel free to fork this repository, explore the code, and suggest improvements or add new features!

## License

This project is open-source and available under the MIT License.
