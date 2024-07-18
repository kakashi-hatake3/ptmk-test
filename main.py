from datetime import datetime
import sqlite3
import sys


class Employee:
    def __init__(self, name, birthday, gender, id_=None):
        self.name = name
        self.birthday = birthday
        self.gender = gender
        self.id_ = id_

    def calculate_age(self):
        birth_date = datetime.strptime(self.birthday, "%Y-%m-%d")
        current_date = datetime.now()
        age = current_date.year - birth_date.year
        if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age

    def insert_employee(self):
        cursor.execute('''
        INSERT INTO employees (name, birthday, gender)
        VALUES (?, ?, ?)
        ''', (self.name, self.birthday, self.gender))
        conn.commit()
        self.id = cursor.lastrowid

    @classmethod
    def create(cls, name, birthday, gender):
        new_instance = cls(name, birthday, gender)
        new_instance.insert_employee()
        return new_instance

    @classmethod
    def create_from_db(cls, table_row):
        new_instance = cls(table_row[1], table_row[2], table_row[3])
        new_instance.id = table_row[0]
        return new_instance

    @classmethod
    def get_table_rows(cls):
        query = """    
                SELECT id, name, birthday, gender
                FROM employees
                GROUP BY name, birthday
                ORDER BY name;
           """
        table_rows = cursor.execute(query).fetchall()
        return [(cls.create_from_db(row), cls.create_from_db(row).calculate_age()) for row in table_rows]

    def __repr__(self):
        return str({'name': self.name, 'birthday': self.birthday, 'gender': self.gender})


conn = sqlite3.connect('people.db')
cursor = conn.cursor()


def algorithm1():
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                      (id INTEGER PRIMARY KEY, name TEXT, birthday TEXT, gender TEXT)''')
    print("Выполняется алгоритм 1")


def algorithm2(name_, birthday_, gender_):
    employee = Employee
    employee.create(name_, birthday_, gender_)
    print("Выполняется алгоритм 2")


def algorithm3():
    employee = Employee
    print(employee.get_table_rows())
    print("Выполняется алгоритм 3")


if __name__ == "__main__":
    if len(sys.argv) != 2 and len(sys.argv) != 5:
        print("Использование: python main.py <номер алгоритма>")
        print("Номер алгоритма может быть 1 или 2")
        sys.exit(1)

    algorithm_number = sys.argv[1]

    if algorithm_number == "1":
        algorithm1()
    elif algorithm_number == "2":
        name, birthday, gender = sys.argv[2:5]
        algorithm2(name, birthday, gender)
    elif algorithm_number == "3":
        algorithm3()
    else:
        print("Неверный номер алгоритма. Допустимые значения: 1 или 2")
        sys.exit(1)
