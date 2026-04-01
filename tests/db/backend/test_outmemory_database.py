import json

from src.db.backend.FileBaseBackend import FileDataBaseJson


def test_create_json_db():
    db = FileDataBaseJson('test.json', 'test123')
    db.create_table('users', id=int, name=str, age=int)
    db.insert_into('users', id=1, name='test', age=10)
    db.insert_into('users', id=2, name='test2', age=20)
    db.insert_into('users', id=3, name='test3', age=30)
    db.delete_from('users', id=1)

    with open('test.json', 'r') as file:
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