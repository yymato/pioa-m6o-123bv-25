from src.db.backend.BaseBackend import DataBase, Table


def test_create():
    db = DataBase('Test123')
    db.create_table('student', id=int, name=str, age=int)

    assert db.name == 'Test123'
    assert list(db.tables.keys()) == ['student']

def test_insert():
    db = DataBase('Test123')
    db.create_table('student', id=int, name=str, age=int)
    db.insert_into('student', id=1, name='ivan', age=20)

    assert db.tables['student'].matrix_data == [[1, 'ivan', 20]]

def test_select_all_rows_():
    db = DataBase('Test123')
    db.create_table('student', id=int, name=str, age=int)
    db.insert_into('student', id=1, name='ivan', age=20)
    db.insert_into('student', id=2, name='ivan2', age=15)
    assert db.select_from('student', return_all_rows=True) == [[1, 'ivan', 20], [2, 'ivan2', 15]]

def test_select_filter():
    db = DataBase('Test123')
    db.create_table('student', id=int, name=str, age=int)
    db.insert_into('student', id=1, name='ivan', age=20)
    db.insert_into('student', id=2, name='ivan2', age=15)

    assert db.select_from('student', id=2) == [[2, 'ivan2', 15]]

def test_update():
    db = DataBase('Test123')
    db.create_table('student', id=int, name=str, age=int)
    db.insert_into('student', id=1, name='ivan', age=20)
    db.update_set('student', 'id', 1, name='Katie')

    assert db.select_from('student', id=1) == [[1, 'Katie', 20]]

def test_delete():
    db = DataBase('Test123')
    db.create_table('student', id=int, name=str, age=int)
    db.insert_into('student', id=1, name='ivan', age=20)
    db.insert_into('student', id=2, name='ivan2', age=15)
    db.delete_from('student', id=1)

    assert db.select_from('student', id=2) == [[2, 'ivan2', 15]]

def test_get_table_header():
    db = DataBase('Test123')
    db.create_table('student', id=int, name=str, age=int)

    assert list(db.get_table_header('student').keys()) == ['id', 'name', 'age']

def test_add_table():
    db = DataBase('Test123')
    table = Table(id={'type': int}, name={'type': str}, age={'type': int})
    db.add_table(table, 'student')

    assert list(db.get_table_header('student').keys()) == ['id', 'name', 'age']
