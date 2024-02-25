# Flask Task Management App

This is a simple task management application built with Flask, SQLAlchemy, and Flask-Login. It allows users to register, login, add tasks, update tasks, delete tasks, and view their tasks.

## Features

- User registration and authentication
- Task management (add, update, delete)
- Task scoring based on impact, ease, and confidence
- Task list sorted by average score

## Installation

1. Clone the repository:

```bash
git clone https://github.com/prathameshdol196/assignment
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

The application uses environment variables for configuration. You can set these variables according to yourself.

Example:

```bash
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///your_database.db 
```

## Routes

### User Authentication

1. Registration:
- `POST /register`: Register a new user.

  - Parameters: `username`, `email`, `password`
  - ```bash
    username = example_user # This is your username
    email = example_user@example.com # This is your email
    password = example_password # This is your password
    ```
  - Example URL: `/register?username=example_username&email=example_user@example.com&password=example_password`

#
2. Login:
- `POST /login`: Login as an existing user.
  - Parameters: `email`, `password`
  - ```bash
    email = example_user@example.com # This is your email used while registration
    password = example_password # This is password you used while registration
    ```
  - Example URl: `/login?email=example_user@example.com&password=example_password`
  
#    
3. Logout
- `GET /logout`: Logout the current user.
  - Example: `/logout`


#
### Task 


1. Get Tasks
- `GET /tasks`: Get all tasks for the current user.
  - Example URL: `/get_tasks`
  
2. Add Task
- `POST /add_task`: Add a new task for the current user.
  - Parameters: `title`, `description`, `impact`, `ease`, `confidance`
  - ```bash
    title = title_of_task  # Must be String
    description = description_of_task  # Must be String
    impact = impact_of_task  # Must be Integer
    ease = ease_of_task  # Must be Integer
    confidence = confidence_of_task  # Must be Integer
    ```
  - Example URL: `/add_task?title=title_of_task&description=description_of_task&impact=impact&ease=ease0&confidence=confidence`

3. Update Task
- `PUT /update_task`: Update an existing task.
  - Parameters: `task_id`, `title`, `description`, `impact`, `ease`, `confidance`
  - ```bash
    task_id = id_of_task  # This field is compulsory
    title = title_of_task  
    description = description_of_task 
    impact = impact_of_task  
    ease = ease_of_task  
    confidence = confidence_of_task  
    ```
  - Example URL: `/update_task?task_id=9&title=this is updated task title of second user&description=this is updated task description of second user&impact=3&ease=5&confidence=9`

4. Delete Task
- `DELETE /delete_task`: Delete an existing task.
- Parameters: `task_id`
- ```bash
  task_id = id_of_task
  ```
  - Example URL: `/delete_task?task_id=id_of_task`
