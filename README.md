# API Documentation: Task Management System

This is a comprehensive documentation for the Task Management System API. The API is designed to manage users, projects, tasks, and comments effectively. Below, you will find setup instructions, API endpoint details, usage examples, and expected responses.

---

## Setup Instructions

### Prerequisites
- Python 3.x installed on your system (3.10+ recommended).
- Django and Django REST Framework installed (leatest versions recommended).
- A PostgreSQL/MySQL database or SQLite (default for development).

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/naye2m/Project_Manager_API.git
   ```
2. Navigate to the project directory:
   ```bash
   cd task-management-api
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure `settings.py`

5. Apply migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the development server:
   ```bash
   python manage.py runserver 127.0.0.1:8000
   ```
7. API will be accessible at `http://127.0.0.1:8000/`.

---


## Postman Configuration File

A Postman collection file, named `Project Manager API.postman_collection.json`, is available in the root directory of the project. This file contains pre-configured requests for all API endpoints, making it easier for you to test the API.

### How to Use the Postman Configuration File:

1. Open Postman.
2. Go to the **File** menu and select **Import**.
3. Click on **Upload Files** and select the `Project Manager API.postman_collection.json` file from the root directory of the project.
4. The collection will be imported into Postman, and you can start testing the endpoints directly.



## API Endpoints

### User Endpoints

#### 1. Register User
- **Method**: POST  
- **URL**: `/api/users/register/`
- **Body**:
  ```json
  {
      "username": "newuser",
      "password": "newpassword",
      "email": "newuser2@example.com",
      "first_name": "John",
      "last_name": "Doe"
  }
  ```
- **Responses**:
  - **201 Created**:
    ```json
    {
        "id": 2,
        "username": "newuser",
        "email": "newuser@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "date_joined": "2025-01-05T20:40:54.217963Z"
    }
    ```
  - **400 Bad Request** (Example):
    ```json
    {
        "username": ["user with this username already exists."]
    }
    ```

#### 2. Login User
- **Method**: POST  
- **URL**: `/api/users/login/`
- **Body**:
  ```json
  {
      "username": "newuser",
      "password": "newpassword"
  }
  ```
- **Responses**:
  - **200 OK**:
    ```json
    {
        "message": "Login successful",
        "token": "<Rest Framework Token>",
        "user_id": 2
    }
    ```
  - **401 Unauthorized**:
    ```json
    {
        "error": "Invalid credentials"
    }
    ```

---

### Project Endpoints

#### 1. Create Project
- **Method**: POST  
- **URL**: `/api/projects/`
- **Headers**:
  ```json
  {
      "Authorization": "Token <your_auth_token>"
  }
  ```
- **Body**:
  ```json
  {
      "name": "New Project",
      "description": "This is a new project."
  }
  ```
- **Responses**:
  - **201 Created**:
    ```json
    {
        "id": 1,
        "name": "New Project",
        "description": "This is a new project.",
        "owner": {
            "id": 2,
            "username": "newuser",
            "email": "newuser@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "date_joined": "2025-01-05T20:40:54.217963Z"
        },
        "created_at": "2025-01-05T21:56:38.198341Z"
    }
    ```
  - **401 Unauthorized**:
    ```json
    {
        "error": "User not authenticated"
    }
    ```

---

### Task Endpoints

#### 1. Create Task
- **Method**: POST  
- **URL**: `/api/tasks/`
- **Body**:
  ```json
  {
      "title": "New Task",
      "description": "This is a new task.",
      "due_date": "2025-01-07T12:00:00Z",
      "priority": "High",
      "assigned_to": 2
  }
  ```
- **Responses**:
  - **201 Created**:
    ```json
    {
        "id": 1,
        "title": "New Task",
        "description": "This is a new task.",
        "status": "To Do",
        "priority": "High",
        "assigned_to": null,
        "project": 1,
        "created_at": "2025-01-05T22:33:27.154869Z",
        "due_date": "2025-01-07T12:00:00Z"
    }
    ```
  - **404 Not Found**:
    ```json
    {
        "error": "Project not found"
    }
    ```

---

### Comment Endpoints

#### 1. Create Comment
- **Method**: POST  
- **URL**: `/api/comments/`
- **Headers**:
  ```json
  {
      "Authorization": "Token <your_auth_token>"
  }
  ```
- **Body**:
  ```json
  {
      "content": "This is a comment."
  }
  ```
- **Responses**:
  - **201 Created**:
    ```json
    {
        "id": 5,
        "content": "This is a comment.",
        "user": {
            "id": 2,
            "username": "newuser",
            "email": "newuser@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "date_joined": "2025-01-05T20:40:54.217963Z"
        },
        "task": 6,
        "created_at": "2025-01-05T22:55:18.674975Z"
    }
    ```
  - **401 Unauthorized**:
    ```json
    {
        "error": "User not authenticated"
    }
    ```

---

## Notes
- All endpoints requiring authentication must include the `Authorization` header with a valid token.
    - You can obtain a token by logging in using the `login` endpoint.
    - Header Format: `Authorization: Token <your_auth_token>`
- Use the `example` payloads as a guide to structure your requests.
