# In-memory база данных
## точка входа в проект [main.py](main.py)
## Поддерживаемые типы данных

| Тип | Описание |
|------|-----------|
| `int` | Целые числа |
| `float` | Числа с плавающей точкой |
| `str` | Строки |
| `bool` | Булевы значения |
| `list` | Списки |
| `dict` | Словари |
| `tuple` | Кортежи |
| `bytes` | Байтовые строки |

## Консольные запросы

### Создание таблицы

```sql
CREATE TABLE table_name (column_name1 type1 column_name2 type2 ...)
```

### Вставка данных

```sql
INSERT INTO table_name (column1 column2 ...) VALUES (value1 value2 ...)
```

### Выборка данных

**Все записи:**
```sql
SELECT FROM table_name WHERE return_all_rows=true
```


**С фильтрацией:**
```sql
SELECT FROM table_name WHERE column=value
```

**Примеры:**
```sql
SELECT FROM users WHERE return_all_rows=true
SELECT FROM users WHERE username='ymato'
SELECT FROM users WHERE age=25 id=1
```
ВНИМАНИЕ начичие WHERE обязательно. Фильтры работают как логическое OR

### Обновление данных

```sql
UPDATE table_name SET column1=value1 column2=value2 ... WHERE filter_column=filter_value
```
ВНИМАНИЕ поддерживается только одно поле для фильтрации

### Удаление данных

```sql
DELETE FROM table_name WHERE column1=value1 column2=value2 ...
```

**Пример:**
```sql
DELETE FROM users WHERE id=123
DELETE FROM users WHERE username='ymato' age=26
```

Фильтры рабоатют как логическое OR

## Использование из кода

### Инициализация базы данных

```python
from backend.BaseBackend import DataBase

db = DataBase("MyDatabase")
```

### Создание таблицы

```python
db.create_table(
    table_name="users",
    id=int,
    username=str,
    age=int,
    is_active=bool,
    tags=list
)
```

### Вставка данных

```python
db.insert_into(
    table_name="users",
    id=1,
    username="john_doe",
    age=30,
    is_active=True,
    tags=["python", "database"]
)
```

### Выборка данных

```python
# Получить все записи
all_users = db.select_from("users", return_all_rows=True)

# Получить записи с фильтрацией
filtered_users = db.select_from(
    "users",
    username="john_doe",
    age=30
)
```

### Обновление данных

```python
db.update_set(
    table_name="users",
    filter_col_name="username",
    filter_col_value="john_doe",
    age=31,
    is_active=False
)
```

### Удаление данных

```python
db.delete_from(
    table_name="users",
    username="john_doe",
    age=31
)
```

### Получение информации о таблице

```python
# Получить список всех таблиц
tables = db.get_names_tables()

# Получить заголовок (структуру) таблицы
header = db.get_table_header("users")
```

![meme.jpeg](images/meme.jpeg)