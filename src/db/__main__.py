from src.db.tui import TUI


# CREATE TABLE users (id int, username str)
# INSERT INTO users (id, username) VALUES (1, 'ymato')
# SELECT FROM users WHERE return_all_rows=true
# UPDATE users SET id=123 WHERE username='ymato'

# SELECT FROM table_name WHERE colum=value Поддерживается только равенство, знаки больше меньше нельзя. Все ыфильтры применяются со знаком или
# DELETE FROM users WHERE id=1

def main():
    app = TUI()
    app.run()


if __name__ == "__main__":
    main()
