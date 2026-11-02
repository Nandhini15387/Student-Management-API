# Student Management REST API

## Project Description

The Student Management REST API is developed using Python Flask and SQLite. It allows users to perform CRUD operations to manage student information.

## Technologies Used

* Python
* Flask
* SQLite
* Postman

## Features

* Add student details.
* View all students.
* View individual student details.
* Update student information.
* Delete student records.
* JSON responses.
* Input validation and error handling.

## API Endpoints

| Method | Endpoint           | Description       |
| ------ | ------------------ | ----------------- |
| GET    | /                  | Welcome message   |
| GET    | /api/students      | Get all students  |
| GET    | /api/students/<id> | Get student by ID |
| POST   | /api/students      | Add a student     |
| PUT    | /api/students/<id> | Update student    |
| DELETE | /api/students/<id> | Delete student    |

## Database

SQLite is used to store student information.

### Student Data Model

* id – Unique student ID
* name – Student name
* email – Student email
* course – Student course

## Installation

1. Clone the repository.

2. Install dependencies:

   pip install -r requirements.txt

3. Run the application:

   python app.py

4. Open http://127.0.0.1:5000

## Developer

Developed as part of the Python Programming Internship.
