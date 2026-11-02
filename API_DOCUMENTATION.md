# Student Management REST API – API Documentation

## 1. Introduction

The Student Management REST API is developed using Python Flask and SQLite. It allows users to create, retrieve, update, and delete student records through HTTP requests.

## 2. Base URL

Local Development:

http://127.0.0.1:5000

## 3. API Endpoints

### Endpoint 1: Welcome Message

* Method: GET
* URL: /
* Description: Displays the API welcome message.

Response:

```json
{
  "message": "Welcome to Student Management API"
}
```

### Endpoint 2: Get All Students

* Method: GET
* URL: /api/students
* Description: Retrieves all student records.

Response:

```json
[
  {
    "id": 1,
    "name": "Nandhini",
    "email": "nandhini@gmail.com",
    "course": "Python Programming"
  }
]
```

### Endpoint 3: Get Student by ID

* Method: GET
* URL: /api/students/1
* Description: Retrieves a particular student using their ID.

Response:

```json
{
  "id": 1,
  "name": "Nandhini",
  "email": "nandhini@gmail.com",
  "course": "Python Programming"
}
```

### Endpoint 4: Add a Student

* Method: POST
* URL: /api/students
* Content-Type: application/json
* Description: Adds a new student record.

Request Body:

```json
{
  "name": "Nandhini",
  "email": "nandhini@gmail.com",
  "course": "Python Programming"
}
```

Response:

```json
{
  "id": 1,
  "message": "Student added successfully"
}
```

Status Code: 201 Created

### Endpoint 5: Update Student

* Method: PUT
* URL: /api/students/1
* Content-Type: application/json
* Description: Updates an existing student's information.

Request Body:

```json
{
  "name": "Nandhini",
  "email": "nandhini@gmail.com",
  "course": "Full Stack Development"
}
```

Response:

```json
{
  "message": "Student updated successfully"
}
```

Status Code: 200 OK

### Endpoint 6: Delete Student

* Method: DELETE
* URL: /api/students/1
* Description: Deletes a student record using their ID.

Response:

```json
{
  "message": "Student deleted successfully"
}
```

Status Code: 200 OK

## 4. Data Model

The Student database contains the following fields:

| Field  | Data Type | Description          |
| ------ | --------- | -------------------- |
| id     | INTEGER   | Primary key          |
| name   | TEXT      | Student name         |
| email  | TEXT      | Unique email address |
| course | TEXT      | Student course       |

## 5. HTTP Status Codes

| Status Code | Description                   |
| ----------- | ----------------------------- |
| 200         | Successful request            |
| 201         | Student created successfully  |
| 400         | Invalid input or missing JSON |
| 404         | Student not found             |
| 409         | Duplicate email address       |

## 6. Error Handling

The API handles errors such as:

* Missing required fields.
* Invalid or missing JSON data.
* Duplicate email addresses.
* Student records not found.

Error Response Example:

```json
{
  "error": "Student not found"
}
```

## 7. Database

SQLite is used as the database to store student records. The database table is automatically created when the application starts.

## 8. Tools and Technologies

* Python
* Flask
* SQLite
* Postman
* Visual Studio Code
* GitHub

## 9. Conclusion

The Student Management REST API successfully implements CRUD operations with database integration, input validation, JSON responses, and error handling.
