from src.db.backend.BaseBackend import DataBase
from src.db.backend.FileBaseBackend import FileDataBaseJson
from src.db.tui import TUI

def main():
    app = TUI()
    app.run()

if __name__ == "__main__":
    main()
