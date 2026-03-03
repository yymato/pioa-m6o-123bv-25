import ast

from backend.BaseBackend import DataBase

# CREATE TABLE users (id int, username str)
# SELECT FROM table_name WHERE colum=value Поддерживается только равенство, знаки больше меньше нельзя. Все ыфильтры применяются со знаком или
# UPDATE users SET email = 'john.new@example.com' WHERE username = 'john_doe';
# DELETE FROM users WHERE id = 3;

a = {
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'list': list,
    'dict': dict,
    'tuple': tuple,
    'bytes': bytes,
}

def strip_bracket(s):
    if s[0] == '(':
        s = s[1:]
    if s[-1] == ')':
        s = s[:-1]
    return s

def main():

    db = DataBase("Base")


    while True:
        user_input = input().split()
        request = user_input.pop(0)
        match request.lower():

            case 'create':
                if user_input[0].lower() == 'table':
                    table_name = user_input[1]

                    try:
                        columns = {col_name.strip(): a[col_type.strip()] for col_name, col_type in user_input[2:]}
                    except KeyError:
                        raise TypeError("Type is not valid")
                    db.create_table(table_name=table_name, **columns)

                else:
                    raise SyntaxError("Not valid request")


            case 'select':
                if user_input[0].lower() == 'from' and user_input[2].lower() == 'where':
                    table_name = user_input[1]
                    filters = user_input[3:]
                    if 'return_all_rows=true' in map(lambda s: s.lower(), filters):
                        print(db.select_from(table_name=table_name,
                                             return_all_rows=True))
                    else:
                        filters = {col: value for col, value in map(lambda s: s.split('='), filters)}
                        print(db.select_from(table_name=table_name,
                                             **filters))
                else:
                    raise SyntaxError("Not valid request")

            case 'insert':
       # INSERT INTO users (username, email, age) VALUES ('john_doe', 'john@example.com', 25);

                if user_input[0].lower() == 'into':
                    table_name = user_input[1]
                    col_names = user_input[2:user_input.lower().index('values')]
                    col_names[0] = col_names[0][1:]
                    try:
                        values = list(map(lambda m: ast.literal_eval(m), user_input[user_input.lower().index('values') + 1:]))
                    except
                    values[-1] = values[-1][:-1]
                    data = {col_name: value for col_name, value in zip(col_names, values)}

                    db.insert_into(table_name=table_name, **data)

                else:
                    raise SyntaxError("Not valid request")






            case 'update':
                pass

            case 'delete':
                pass


if __name__ == "__main__":
    main()