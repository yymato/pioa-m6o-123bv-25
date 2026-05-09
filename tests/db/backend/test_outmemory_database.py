import ast
import csv
import json
import os

from src.db.backend.FileBaseBackend import FileDataBaseJson, FileDataBaseCSV


def test_create_json_db(tmp_path):
    file_path = tmp_path / "test.json"
    db = FileDataBaseJson(file_path, 'test123')
    db.create_table('users', id=int, name=str, age=int)
    db.insert_into('users', id=1, name='test', age=10)
    db.insert_into('users', id=2, name='test2', age=20)
    db.insert_into('users', id=3, name='test3', age=30)
    db.delete_from('users', id=1)

    with open(file_path, 'r') as file:
        data = json.load(file)
    assert data == {"name": "test123",
                    "tables": [
                        {"table_name": "users",
                        "table":
                             {"rows_len": 3,
                              "matrix_data": [[2, "test2", 20],
                                              [3, "test3", 30]],
                              "table_header": {"id": {"type": "int", "index": 0},
                                               "name": {"type": "str", "index": 1},
                                               "age": {"type": "int", "index": 2}}}}]}

def test_open_json_db(tmp_path):
    file_path = tmp_path / "test.json"
    file_path.write_text("""{"name": "test123", "tables": [{"table": {"rows_len": 3, "matrix_data": [[2, "test2", 20], [3, "test3", 30]], "table_header": {"id": {"type": "int", "index": 0}, "name": {"type": "str", "index": 1}, "age": {"type": "int", "index": 2}}}, "table_name": "users"}]}""", encoding='utf-8')

    assert file_path.exists()
    assert file_path.is_file()

    db = FileDataBaseJson(file_path)
    db.open_db()
    data = db.select_from('users', return_all_rows=True)
    assert data == [[2, 'test2', 20], [3, 'test3', 30]]


def test_create_csv_db(tmp_path):
    file_path = tmp_path
    file_path.mkdir(exist_ok=True)

    db = FileDataBaseCSV(file_path)
    db.create_table('users', id=int, name=str, age=int)
    db.insert_into('users', id=1, name='test', age=10)
    db.insert_into('users', id=2, name='test2', age=20)
    db.insert_into('users', id=3, name='test3', age=30)
    db.delete_from('users', id=1)

    db.create_table('students', id=int, name=str, age=int)
    db.insert_into('students', id=1, name='test', age=10)
    db.insert_into('students', id=2, name='test2', age=20)
    db.insert_into('students', id=3, name='test3', age=30)
    db.delete_from('students', id=1)

    with open(os.path.join(file_path, 'users.csv'), 'r') as file:
        data = csv.reader(file)
        header = ast.literal_eval('{' + ','.join(next(data)) + '}')
        assert header == {'id': {'type': 'int', 'index': 0},
                          "name": {'type': 'str', 'index': 1},
                          'age': {'type': 'int', 'index': 2}}
        assert list(data) == [['2', 'test2', '20'], ['3', 'test3', '30']]

    with open(os.path.join(file_path, 'students.csv'), 'r') as file:
        data = csv.reader(file)
        header = ast.literal_eval('{' + ','.join(next(data)) + '}')
        assert header == {'id': {'type': 'int', 'index': 0},
                          "name": {'type': 'str', 'index': 1},
                          'age': {'type': 'int', 'index': 2}}
        assert list(data) == [['2', 'test2', '20'], ['3', 'test3', '30']]

def test_open_csv_db(tmp_path):
    file_path = tmp_path
    file_path.mkdir(exist_ok=True)

    db = FileDataBaseCSV(file_path)
    db.create_table('users', id=int, name=str, age=int)
    db.insert_into('users', id=1, name='test', age=10)
    db.insert_into('users', id=2, name='test2', age=20)
    db.insert_into('users', id=3, name='test3', age=30)
    db.delete_from('users', id=1)

    db.create_table('students', id=int, name=str, age=int)
    db.insert_into('students', id=1, name='test', age=10)
    db.insert_into('students', id=2, name='test2', age=20)
    db.insert_into('students', id=3, name='test3', age=30)
    db.delete_from('students', id=1)

    db2 = FileDataBaseCSV(file_path)
    db2.open_db()
    assert db2.select_from('students', return_all_rows=True) == \
           [['2', 'test2', '20'], ['3', 'test3', '30']]

    assert db2.select_from('users', return_all_rows=True) == \
           [['2', 'test2', '20'], ['3', 'test3', '30']]

    db2.insert_into('students', id=1, name='test', age=10)
    assert db2.select_from('students', return_all_rows=True) == [['2', 'test2', '20'], ['3', 'test3', '30'],
                                                                 [1, 'test', 10]]