import ast
import csv
import json
import os

from src.db.backend.BaseBackend import DataBase, Table


class FileDataBaseJson(DataBase):
    def __init__(self, path, name='Unknown'):
        super().__init__(name)
        self.path = path

    def _to_dict(self):
        data = {'name': self.name, 'tables': []}
        for table_name, table in self.tables.items():
            data['tables'].append({'table': table.to_dict(), 'table_name': table_name})

        return data

    def open_db(self):
        with open(self.path, "r") as f:
            data = json.load(f)
            self._from_dict(data)

    def save_db(self):
        with open(self.path, "w") as f:
            json.dump(self._to_dict(), f)

    def _from_dict(self, data):
        self.name = data['name']
        self.tables = {}
        for i in data['tables']:
            self.tables[i['table_name']] = Table(from_dict=i['table'])

    def add_table(self, *args, **kwargs):
        super().add_table(*args, **kwargs)
        self.save_db()

    def create_table(self, *args, **kwargs):
        super().create_table(*args, **kwargs)
        self.save_db()

    def delete_from(self, *args, **kwargs):
        super().delete_from(*args, **kwargs)
        self.save_db()

    def insert_into(self, *args, **kwargs):
        super().insert_into(*args, **kwargs)
        self.save_db()

    def update_set(self, *args, **kwargs):
        super().update_set(*args, **kwargs)
        self.save_db()

    def set_table_name(self, *args, **kwargs):
        super().set_table_name(*args, **kwargs)
        self.save_db()


class FileDataBaseCSV(DataBase):
    def __init__(self, directory, name='Unknown'):
        super().__init__(name)
        self.directory = directory
        os.makedirs(os.path.abspath(directory), exist_ok=True)

    def save_db(self):
        for table_name, table in self.tables.items():
            data = table.to_dict()
            matrix = data['matrix_data']
            header = [[f'{key}: {data['table_header'][key].__repr__()}' for key in table.table_header]]
            data = header + table.matrix_data
            print(data)
            with open(f"{self.directory}/{table_name}.csv", "w+") as f:
                csv.writer(f).writerows(data)

    def open_db(self):
        files_paths = []
        print(os.listdir(self.directory))
        for path in os.listdir(self.directory):
            if path.endswith(".csv"):
                files_paths.append(os.path.join(self.directory, path))

        print(files_paths)
        for path in files_paths:
            with open(path, "r") as f:
                data = csv.reader(f)

                print('{' + ','.join(next(data)) + '}')
                header = ast.literal_eval('{' + ','.join(next(data)) + '}')
                data_matrix = list(map(list, data))

                table = Table(from_dict={
                    'table_header': header,
                    'matrix_data': data_matrix,
                    'rows_len': len(header)
                })
                self.tables[path.split("\\")[-1][:-4]] = table
                print(path)

        print(self.tables)

    def create_table(self, *args, **kwargs):
        super().create_table(*args, **kwargs)
        self.save_db()

    def insert_into(self, *args, **kwargs):
        super().insert_into(*args, **kwargs)
        self.save_db()

    def update_set(self, *args, **kwargs):
        super().update_set(*args, **kwargs)
        self.save_db()

    def delete_from(self, table_name, **filter_cols):
        super().delete_from(table_name, **filter_cols)
        self.save_db()

