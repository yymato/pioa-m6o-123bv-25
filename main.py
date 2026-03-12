import ast
from backend.BaseBackend import DataBase


# CREATE TABLE users (id int, username str)
# INSERT INTO users (id, username) VALUES (1, 'ymato')
# SELECT FROM users WHERE return_all_rows=true
# UPDATE users SET id=123 WHERE username='ymato'

# SELECT FROM table_name WHERE colum=value Поддерживается только равенство, знаки больше меньше нельзя. Все ыфильтры применяются со знаком или
# DELETE FROM users WHERE id=1

dict_types = {
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
    if s[0] == ',':
        s = s[1:]
    if s[-1] == ',':
        s = s[:-1]
    return s


def main():
    db = DataBase("Base")

    while True:
        user_input = input()
        if user_input == '\n' or user_input == '':
            continue
        user_input = user_input.split()

        request = user_input.pop(0)
        match request.lower():

            case 'create':
                if user_input[0].lower() == 'table':
                    table_name = user_input[1]

                    try:
                        columns = {strip_bracket(user_input[2 + i]): dict_types[strip_bracket(user_input[2 + 1 + i])]
                                   for i in range(0, len(user_input[2:]), 2)}
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
                        print('\t'.join(db.get_table_header(table_name)))
                        print('\n'.join(map(lambda lst: '\t'.join(map(str, lst)),
                                            db.select_from(table_name=table_name, return_all_rows=True))))
                    else:
                        filters = {col: ast.literal_eval(value) for col, value in map(lambda s: s.split('='), filters)}
                        print('\t'.join(db.get_table_header(table_name)))
                        print('\n'.join(map(lambda lst: '\t'.join(map(str, lst)), db.select_from(table_name=table_name,
                                             **filters))))
                else:
                    raise SyntaxError("Not valid request")

            case 'insert':

                if user_input[0].lower() == 'into':
                    table_name = user_input[1]
                    col_names = user_input[2:list(map(lambda s: s.lower(), user_input)).index('values')]
                    col_names = list(map(strip_bracket, col_names))
                    try:
                        print(user_input[list(map(lambda s: s.lower(), user_input)).index('values') + 1:])
                        values = list(map(strip_bracket,
                                          user_input[list(map(lambda s: s.lower(), user_input)).index('values') + 1:]))
                        values = list(map(ast.literal_eval, values))
                    except ValueError:
                        raise ValueError("Value is not valid")
                    data = {col_name: value for col_name, value in zip(col_names, values)}

                    db.insert_into(table_name=table_name, **data)

                else:
                    raise SyntaxError("Not valid request")

            case 'update':
                table_name = user_input[0]
                where_index = list(map(lambda s: s.lower(), user_input)).index('where')
                print(user_input, where_index)
                data = {col: ast.literal_eval(value) for col, value in map(lambda s: s.split('='),
                                                                           user_input[2:where_index])}
                filter_col = user_input[where_index + 1].split('=')[0]
                filter_val = ast.literal_eval(user_input[where_index + 1].split('=')[1])

                db.update_set(table_name=table_name,
                              filter_col_name=filter_col,
                              filter_col_value=filter_val, **data)

            case 'delete':
                if user_input[0].lower() == 'from':
                    table_name = user_input[1]
                    print(user_input)
                    filters = {col: ast.literal_eval(value) for col, value in
                               map(lambda s: s.split('='), user_input[3:])}
                    db.delete_from(table_name=table_name, **filters)


if __name__ == "__main__":
    main()
