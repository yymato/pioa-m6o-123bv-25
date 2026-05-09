from src.db.tui import TUI


def test_tui_create(monkeypatch):
    commands = iter(['CREATE TABLE users (id int name str age int)', 'exit'])
    def f(x=''):
        return next(commands)
    monkeypatch.setattr('builtins.input', f)

    app = TUI()
    app.run()

    assert list(app.db.tables.keys()) == ['users']

def test_tui_insert(monkeypatch):
    commands = iter(['CREATE TABLE users (id int name str age int)',
                     "INSERT INTO users (id name age) VALUES (1 'Katie' 18)",
                     'exit'])

    def f(x=''):
        return next(commands)

    monkeypatch.setattr('builtins.input', f)

    app = TUI()
    app.run()

    assert app.db.tables['users'].matrix_data == [[1, 'Katie', 18]]


def test_tui_select_filter(monkeypatch, capsys):
    commands = iter(['CREATE TABLE users (id int name str age int)',
                     "INSERT INTO users (id name age) VALUES (1 'Katie' 18)",
                     "INSERT INTO users (id name age) VALUES (2 'ivan' 20)",
                    'SELECT FROM users WHERE id=1',
                     'exit'])

    def f(x=''):
        return next(commands)

    monkeypatch.setattr('builtins.input', f)

    app = TUI()
    app.run()

    captured = capsys.readouterr()
    assert captured.out == """id\tname\tage\n1\tKatie\t18\n"""

def test_tui_select_all(monkeypatch, capsys):
    commands = iter(['CREATE TABLE users (id int name str age int)',
                     "INSERT INTO users (id name age) VALUES (1 'Katie' 18)",
                     "INSERT INTO users (id name age) VALUES (2 'ivan' 20)",
                     'SELECT FROM users WHERE return_all_rows=True',
                     'exit'])

    def f(x=''):
        return next(commands)

    monkeypatch.setattr('builtins.input', f)

    app = TUI()
    app.run()

    captured = capsys.readouterr()
    assert captured.out == """id\tname\tage\n1\tKatie\t18\n2\tivan\t20\n"""


def test_tui_update(monkeypatch, capsys):
    commands = iter(['CREATE TABLE users (id int name str age int)',
                     "INSERT INTO users (id name age) VALUES (1 'Katie' 18)",
                     "INSERT INTO users (id name age) VALUES (2 'ivan' 20)",
                     "UPDATE users SET age=29 WHERE id=1",
                     'SELECT FROM users WHERE return_all_rows=True',
                     'exit'])

    def f(x=''):
        return next(commands)

    monkeypatch.setattr('builtins.input', f)

    app = TUI()
    app.run()

    captured = capsys.readouterr()
    assert captured.out == """id\tname\tage\n1\tKatie\t29\n2\tivan\t20\n"""

def test_tui_delete(monkeypatch, capsys):
    commands = iter(['CREATE TABLE users (id int name str age int)',
                     "INSERT INTO users (id name age) VALUES (1 'Katie' 18)",
                     "INSERT INTO users (id name age) VALUES (2 'ivan' 20)",
                     "DELETE FROM users WHERE id=1",
                     'SELECT FROM users WHERE return_all_rows=True',
                     'exit'])

    def f(x=''):
        return next(commands)

    monkeypatch.setattr('builtins.input', f)

    app = TUI()
    app.run()

    captured = capsys.readouterr()
    assert captured.out == """id\tname\tage\n2\tivan\t20\n"""


def test_tui_empty_input_ignored_then_create(monkeypatch):
    commands = iter(['', '\n', 'CREATE TABLE users (id int name str)', 'exit'])
    def f(x=''):
        return next(commands)
    monkeypatch.setattr('builtins.input', f)

    app = TUI()
    app.run()
    assert list(app.db.tables.keys()) == ['users']


def test_tui_create_invalid_type_prints_error(monkeypatch, capsys):
    commands = iter(['CREATE TABLE test (col blob)', 'exit'])
    def f(x=''):
        return next(commands)
    monkeypatch.setattr('builtins.input', f)

    TUI().run()
    captured = capsys.readouterr()
    assert "Type is not valid" in captured.out


def test_tui_select_missing_where_raises_index_error(monkeypatch, capsys):
    commands = iter(['CREATE TABLE users (id int)', 'SELECT FROM users', 'exit'])
    def f(x=''):
        return next(commands)
    monkeypatch.setattr('builtins.input', f)

    TUI().run()
    captured = capsys.readouterr()
    assert "list index out of range" in captured.out


def test_tui_insert_with_list_value(monkeypatch, capsys):
    commands = iter([
        'CREATE TABLE items (id int tags list)',
        "INSERT INTO items (id tags) VALUES (1 [1,2,3])",
        'SELECT FROM items WHERE return_all_rows=True',
        'exit'
    ])
    def f(x=''):
        return next(commands)
    monkeypatch.setattr('builtins.input', f)

    app = TUI()
    app.run()
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n') == [
        "id\ttags",
        "1\t[1, 2, 3]"
    ]


def test_tui_insert_with_dict_value(monkeypatch, capsys):
    commands = iter([
        'CREATE TABLE config (id int meta dict)',
        "INSERT INTO config (id meta) VALUES (1 {'a':1})",
        'SELECT FROM config WHERE return_all_rows=True',
        'exit'
    ])
    def f(x=''):
        return next(commands)
    monkeypatch.setattr('builtins.input', f)

    app = TUI()
    app.run()
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n') == [
        "id\tmeta",
        "1\t{'a': 1}"
    ]


def test_tui_select_multiple_filters(monkeypatch, capsys):
    commands = iter([
        'CREATE TABLE users (id int name str)',
        "INSERT INTO users (id name) VALUES (1 'Katie')",
        "INSERT INTO users (id name) VALUES (2 'ivan')",
        "SELECT FROM users WHERE id=2 name='ivan'",
        'exit'
    ])
    def f(x=''):
        return next(commands)
    monkeypatch.setattr('builtins.input', f)

    app = TUI()
    app.run()
    captured = capsys.readouterr()
    # Должна вернуться только одна строка
    assert captured.out.strip().split('\n') == [
        "id\tname",
        "2\tivan"
    ]


def test_tui_update_multiple_set_columns(monkeypatch, capsys):
    commands = iter([
        'CREATE TABLE users (id int name str age int)',
        "INSERT INTO users (id name age) VALUES (1 'Katie' 18)",
        "UPDATE users SET age=29 name='NewName' WHERE id=1",
        'SELECT FROM users WHERE return_all_rows=True',
        'exit'
    ])
    def f(x=''):
        return next(commands)
    monkeypatch.setattr('builtins.input', f)

    app = TUI()
    app.run()
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n') == [
        "id\tname\tage",
        "1\tNewName\t29"
    ]



