from src.db.backend.BaseBackend import DataBase
from src.db.backend.FileBaseBackend import FileDataBase
from src.db.tui import TUI

def main():
    # app = TUI()
    # app.run()

    db = FileDataBase('test.json', 'Test123')
    db.open_db()
    print(db.select_from('users', return_all_rows=True))

if __name__ == "__main__":
    main()
