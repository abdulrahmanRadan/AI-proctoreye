import sqlite3

class Student:
    table_name = 'students'

    def __init__(self, db_name=":memory:"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS students (
            StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
            StudentName TEXT,
            Number TEXT,
            College TEXT,
            Level TEXT,
            Specialization TEXT,
            ImagePath TEXT
        )
        """
        self.execute_query(query)

    def execute_query(self, query, params=()):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        connection.close()

    def create(self, **kwargs):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?'] * len(kwargs))
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, tuple(kwargs.values()))

    def all(self, **filters):
        query = f"SELECT * FROM {self.table_name}"
        if filters:
            conditions = ' AND '.join([f"{key} = ?" for key in filters])
            query += f" WHERE {conditions}"
            return self.execute_read_query(query, tuple(filters.values()))
        return self.execute_read_query(query)

    def first(self, **filters):
        result = self.all(**filters)
        return result[0] if result else None

    def last(self, **filters):
        result = self.all(**filters)
        return result[-1] if result else None

    def find(self, **kwargs):
        query = f"SELECT * FROM {self.table_name}"
        if kwargs:
            conditions = ' AND '.join([f"{key} = ?" for key in kwargs])
            query += f" WHERE {conditions}"
            return self.execute_read_query(query, tuple(kwargs.values()))
        return None

    def update(self, identifier, **kwargs):
        set_clause = ', '.join([f"{key} = ?" for key in kwargs])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE StudentID = ?"
        self.execute_query(query, tuple(kwargs.values()) + (identifier,))

    def delete(self, **kwargs):
        query = f"DELETE FROM {self.table_name} WHERE "
        conditions = ' AND '.join([f"{key} = ?" for key in kwargs])
        query += conditions
        self.execute_query(query, tuple(kwargs.values()))

    def exists(self, **kwargs):
        query = f"SELECT COUNT(*) FROM {self.table_name} WHERE "
        conditions = ' AND '.join([f"{key} = ?" for key in kwargs])
        query += conditions
        result = self.execute_read_query(query, tuple(kwargs.values()))
        return result[0][0] > 0

    def execute_read_query(self, query, params=()):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        connection.close()
        return result