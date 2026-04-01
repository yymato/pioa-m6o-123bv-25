from src.db.tui import TUI


def test_tui_create(monkeypatch):
    commands = iter(['2', 'CREATE TABLE users (id int name str age int)', 'exit'])
    def f(x=''):
        return next(commands)
    monkeypatch.setattr('builtins.input', f)

    app = TUI()
    app.run()

    assert list(app.db.tables.keys()) == ['users']

def test_tui_insert(monkeypatch):
    commands = iter(['2', 'CREATE TABLE users (id int name str age int)',
                     "INSERT INTO users (id name age) VALUES (1 'Katie' 18)",
                     'exit'])

    def f(x=''):
        return next(commands)

    monkeypatch.setattr('builtins.input', f)

    app = TUI()
    app.run()

    assert app.db.tables['users'].matrix_data == [[1, 'Katie', 18]]


def test_tui_select_filter(monkeypatch, capsys):
    commands = iter(['2', 'CREATE TABLE users (id int name str age int)',
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
    commands = iter(['2', 'CREATE TABLE users (id int name str age int)',
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
    commands = iter(['2', 'CREATE TABLE users (id int name str age int)',
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
    commands = iter(['2', 'CREATE TABLE users (id int name str age int)',
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

