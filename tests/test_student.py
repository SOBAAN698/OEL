import pytest
from unittest.mock import MagicMock, patch
from app.services.student_service import StudentService
from app.models.student_model import Student

@patch("app.services.student_service.get_connection")
def test_add_student_success(mock_get_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.lastrowid = 42
    
    student = Student(name="John Doe", student_class="10th", age=16)
    result = StudentService.add_student(student)
    
    assert result.id == 42
    assert result.name == "John Doe"
    assert result.student_class == "10th"
    assert result.age == 16
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO students (name, class, age) VALUES (%s, %s, %s)",
        ("John Doe", "10th", 16)
    )

def test_add_student_empty_name():
    student = Student(name="", student_class="10th", age=16)
    with pytest.raises(ValueError, match="Student name cannot be empty."):
        StudentService.add_student(student)

def test_add_student_invalid_age():
    student = Student(name="John Doe", student_class="10th", age=-5)
    with pytest.raises(ValueError, match="Student age must be a positive integer."):
        StudentService.add_student(student)

@patch("app.services.student_service.get_connection")
def test_get_all_students(mock_get_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [
        {"id": 1, "name": "Alice", "class": "10th", "age": 15},
        {"id": 2, "name": "Bob", "class": "11th", "age": 16}
    ]
    
    students = StudentService.get_all_students()
    
    assert len(students) == 2
    assert students[0].name == "Alice"
    assert students[1].name == "Bob"
    assert students[0].id == 1
    assert students[1].student_class == "11th"

@patch("app.services.student_service.get_connection")
def test_update_student_success(mock_get_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    student = Student(student_id=1, name="Alice Cooper", student_class="10th", age=16)
    result = StudentService.update_student(student)
    
    assert result is True
    mock_cursor.execute.assert_called_once_with(
        "UPDATE students SET name = %s, class = %s, age = %s WHERE id = %s",
        ("Alice Cooper", "10th", 16, 1)
    )

@patch("app.services.student_service.get_connection")
def test_delete_student_success(mock_get_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    result = StudentService.delete_student(12)
    
    assert result is True
    mock_cursor.execute.assert_called_once_with("DELETE FROM students WHERE id = %s", (12,))
