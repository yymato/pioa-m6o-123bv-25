from src.db.tui import TUI


def test_tui_json(monkeypatch, capsys, tmp_path):
    file_path = tmp_path / "test.json"
    file_path.write_text(
        """{"name": "test123", "tables": [{"table": {"rows_len": 3, "matrix_data": [[2, "test2", 20], [3, "test3", 30]], "table_header": {"id": {"type": "int", "index": 0}, "name": {"type": "str", "index": 1}, "age": {"type": "int", "index": 2}}}, "table_name": "users"}]}""",
        encoding='utf-8')

    commands = iter(['1',
                     file_path,
                     'SELECT FROM users WHERE return_all_rows=True',
                     'exit'])

    def f(x=''):
        return next(commands)

    monkeypatch.setattr('builtins.input', f)

    app = TUI()
    app.run()

    captured = capsys.readouterr()
    assert captured.out == """id\tname\tage\n2\ttest2\t20\n3\ttest3\t30\n"""

def test_open_json_db(monkeypatch, capsys, tmp_path):
    file_path = tmp_path / "test.json"

    commands = iter(['1',
                     file_path,
                     'CREATE TABLE users (id int name str age int)',
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
