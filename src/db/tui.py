import ast
import os

from src.db.backend.BaseBackend import DataBase
from src.db.backend.FileBaseBackend import FileDataBaseJson, FileDataBaseCSV


class TUI:
    def __init__(self):
        self.dict_types = {
                        'int': int,
                        'float': float,
                        'str': str,
                        'bool': bool,
                        'list': list,
                        'dict': dict,
                        'tuple': tuple,
                        'bytes': bytes,
                    }


    def run(self):
        user_input = input('Выберите с какой бд работать: \n1. Файловая Json\n2. Файловая CSV\n3. Inmemory\n')
        if user_input == '1':
            path = input('Введите путь до файла .json')
            self.db = FileDataBaseJson(path)
            if os.path.exists(path):
                self.db.open_db()
            self.main_loop()
        elif user_input == '3':
            path = input('Введите путь до ирректории с файлами.csv')
            self.db = FileDataBaseCSV(path)
            if os.path.exists(path):
                self.db.open_db()
            self.main_loop()
        elif user_input == '2':
            self.db = DataBase('Base')
            self.main_loop()

    def main_loop(self):
        while True:
            try:
                user_input = input()
                if user_input == '\n' or user_input == '':
                    continue
                user_input = user_input.split()

                request = user_input.pop(0)
                match request.lower():
                    case 'create':
                        self._create_table(user_input)
                    case 'select':
                        self._select(user_input)
                    case 'insert':
                        self._insert(user_input)
                    case 'update':
                        self._update(user_input)
                    case 'delete':
                        self._delete(user_input)
                    case 'exit':
                        break
            except Exception as e:
                print(e)

    def _create_table(self, user_input):
        if user_input[0].lower() == 'table':
            table_name = user_input[1]
            try:
                columns = {}
                pairs_columns_name_type= user_input[2:]
                for i in range(0, len(pairs_columns_name_type), 2):
                    columns[self.strip_bracket(pairs_columns_name_type[i])] = \
                    self.dict_types[self.strip_bracket(pairs_columns_name_type[i + 1])]
            except KeyError:
                raise TypeError("Type is not valid")
            self.db.create_table(table_name=table_name, **columns)
        else:
            raise SyntaxError("Not valid request")

    def _select(self, user_input):
        if user_input[0].lower() == 'from' and user_input[2].lower() == 'where':
            table_name = user_input[1]
            filters = user_input[3:]
            if 'return_all_rows=true' in map(lambda s: s.lower(), filters):
                print('\t'.join(self.db.get_table_header(table_name)))
                print('\n'.join(map(lambda lst: '\t'.join(map(str, lst)),
                                    self.db.select_from(table_name=table_name, return_all_rows=True))))
            else:
                filters = {col: ast.literal_eval(value) for col, value in map(lambda s: s.split('='), filters)}
                print('\t'.join(self.db.get_table_header(table_name)))
                print('\n'.join(map(lambda lst: '\t'.join(map(str, lst)), self.db.select_from(table_name=table_name,
                                                                                         **filters))))
        else:
            raise SyntaxError("Not valid request")

    def _insert(self, user_input):
        if user_input[0].lower() != 'into':
            raise SyntaxError("Not valid request")

        table_name = user_input[1]
        lowered = [s.lower() for s in user_input]

        try:
            values_idx = lowered.index('values')
        except ValueError:
            raise SyntaxError("Missing VALUES clause")

        col_names = list(map(self.strip_bracket, user_input[2:values_idx]))

        raw_values = user_input[values_idx + 1:]

        if raw_values[0].startswith('('):
            raw_values[0] = raw_values[0][1:]
        if raw_values[-1].endswith(')'):
            raw_values[-1] = raw_values[-1][:-1]

        values_str = ' '.join(raw_values)
        tokens = []
        current = ''
        depth_paren = 0
        depth_square = 0
        depth_curly = 0

        for c in values_str:
            if c == '(':
                depth_paren += 1
                current += c
            elif c == ')':
                depth_paren -= 1
                current += c
            elif c == '[':
                depth_square += 1
                current += c
            elif c == ']':
                depth_square -= 1
                current += c
            elif c == '{':
                depth_curly += 1
                current += c
            elif c == '}':
                depth_curly -= 1
                current += c
            elif c == ' ':
                if depth_paren == 0 and depth_square == 0 and depth_curly == 0:
                    if current:
                        tokens.append(current)
                        current = ''
                else:
                    current += c
            else:
                current += c

        if current:
            tokens.append(current)

        try:
            values = [ast.literal_eval(tok) for tok in tokens]
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Invalid value literal: {e}")

        if len(col_names) != len(values):
            raise ValueError("Number of columns does not match number of values")

        data = dict(zip(col_names, values))
        self.db.insert_into(table_name=table_name, **data)

    def _update(self, user_input):
        table_name = user_input[0]
        where_index = list(map(lambda s: s.lower(), user_input)).index('where')
        data = {col: ast.literal_eval(value) for col, value in map(lambda s: s.split('='),
                                                                   user_input[2:where_index])}
        filter_col = user_input[where_index + 1].split('=')[0]
        filter_val = ast.literal_eval(user_input[where_index + 1].split('=')[1])

        self.db.update_set(table_name=table_name,
                      filter_col_name=filter_col,
                      filter_col_value=filter_val, **data)

    def _delete(self, user_input):
        if user_input[0].lower() == 'from':
            table_name = user_input[1]
            filters = {col: ast.literal_eval(value) for col, value in
                       map(lambda s: s.split('='), user_input[3:])}
            self.db.delete_from(table_name=table_name, **filters)

    def strip_bracket(self, s):
        if s[0] == '(':
            s = s[1:]
        if s[-1] == ')':
            s = s[:-1]
        if s[0] == ',':
            s = s[1:]
        if s[-1] == ',':
            s = s[:-1]
        return s