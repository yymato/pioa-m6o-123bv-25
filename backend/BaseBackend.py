class DataBase:
    def __init__(self, name):
        self.tables = {}
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        self.name = name

    def add_table(self, table, table_name: str):
        if isinstance(table, Table) and isinstance(table_name, str):
            if table_name in self.tables:
                raise Exception(f"Table {table_name} already exists")
            else:
                self.tables[table_name] = table
        else:
            raise TypeError("table must be a Table\ntable_name must be a string")

    def create_table(self, table_name: str="unknown", **table_header):
        for key in table_header:
            table_header[key] = {"type": table_header[key]}
        table = Table(**table_header)
        self.tables[table_name] = table

    def select_from(self, table_name: str, return_all_rows=False, **filter_cols):
        if table_name in self.tables:
            return self.tables[table_name].select(return_all_rows, **filter_cols)
        else:
            raise Exception("Unknown table: {}".format(table_name))

    def delete_from(self, table_name: str, **filter_cols):
        if table_name in self.tables:
            self.tables[table_name].delete(**filter_cols)
        else:
            raise Exception("Unknown table: {}".format(table_name))

    def insert_into(self, table_name, **cols):
        if table_name in self.tables:
            self.tables[table_name].add(**cols)
        else:
            raise Exception("Unknown table: {}".format(table_name))

    def update_set(self, table_name: str, filter_col_name, filter_col_value, **cols):
        if table_name in self.tables:
            self.tables[table_name].update(filter_col_name=filter_col_name, filter_col_value=filter_col_value, **cols)
        else:
            raise Exception("Unknown table: {}".format(table_name))

    def get_names_tables(self):
        return list(self.tables.keys())

    def set_table_name(self, old_table_name, new_table_name):
        self.tables[old_table_name] = new_table_name

    def get_table_header(self, table_name: str):
        if table_name in self.tables:
            return self.tables[table_name].get_header()


class Table:
    def __init__(self, **table_header):
        self.table_header = {}
        self.matrix_data = []

        for i, (col_name, col_property) in enumerate(table_header.items()):
            col_property["index"] = i
            self.table_header[col_name] = col_property

        self.rows_len = len(self.table_header)

    def select(self, return_all_rows=False, **filter_cols):
        result = list()
        if return_all_rows:
            return self.matrix_data.copy()

        for row in self.matrix_data:

            for col_name, value in filter_cols.items():
                if col_name in self.table_header:
                    index = self.table_header[col_name]["index"]
                    if row[index] == self.check_type(col_name, value):
                        result.append(row)
                        break

        return result

    def add(self, **cols):
        row = [None for _ in range(self.rows_len)]
        for col_name, value in cols.items():
            if col_name in self.table_header:
                col_index = self.table_header[col_name]["index"]
                row[col_index] = self.check_type(col_name, value)
            else:
                raise Exception("Unknown column: {}".format(col_name))
        self.matrix_data.append(row)

    def delete(self, **filter_cols):
        for col_name, value in filter_cols.items():
            if col_name in self.table_header:
                index = self.table_header[col_name]["index"]
                for row in self.matrix_data:
                    if row[index] == self.check_type(col_name, value):
                        self.matrix_data.remove(row)
            else:
                raise Exception("Unknown column: {}".format(col_name))

    def update(self, filter_col_name, filter_col_value, **cols):
        if filter_col_name in self.table_header:
            filter_col_index = self.table_header[filter_col_name]["index"]
            for row in self.matrix_data:
                if row[filter_col_index] == self.check_type(filter_col_name, filter_col_value):
                    for col_name, value in cols.items():
                        index = self.table_header[col_name]["index"]
                        row[index] = self.check_type(col_name, value)

        else:
            raise Exception("Unknown column: {}".format(filter_col_name))

    def check_type(self, col_name: str, value):
        if isinstance(value, self.table_header[col_name]["type"]):
            return value
        else:
            raise TypeError('value must be a {}'.format(self.table_header[col_name]["type"]))

    def get_header(self):
        return self.table_header.copy()
