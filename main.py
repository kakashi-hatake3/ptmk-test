import random
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

    def many_insert(self):
        start_time = datetime.now()
        insert_query = '''
        INSERT INTO employees (name, birthday, gender)
        VALUES (?, ?, ?)
        '''
        employees = []
        for i in range(100):
            employees.append({'name': 'Franklin Ron Hillary', 'birthday': '1985-05-15', 'gender': 'Male'})
        data_to_insert = [(emp["name"], emp["birthday"], emp["gender"]) for emp in employees]
        cursor.executemany(insert_query, data_to_insert)
        data_to_insert.clear()
        employees.clear()
        conn.commit()
        for i in range(10000):
            for j in range(100):
                employees.append({'name': f'{chr(random.randint(ord("A"), ord("Z")))}ranklin Ron Hillary',
                                  'birthday': '1995-07-20',
                                  'gender': f'{random.choice(["Male", "Female"])}'})
            data_to_insert = [(emp["name"], emp["birthday"], emp["gender"]) for emp in employees]
            cursor.executemany(insert_query, data_to_insert)
            data_to_insert.clear()
            employees.clear()
            conn.commit()
        end_time = datetime.now() - start_time
        print(end_time)

    @classmethod
    def create_from_db(cls, table_row):
        new_instance = cls(table_row[1], table_row[2], table_row[3])
        new_instance.id = table_row[0]
        return new_instance

    @classmethod
    def get_table_rows(cls):
        stmt = """    
                SELECT id, name, birthday, gender
                FROM employees
                GROUP BY name, birthday
                ORDER BY name;
           """
        table_rows = cursor.execute(stmt).fetchall()
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


"""
    0:14:03.938288 - время заполнения бд
"""


def algorithm4():
    employee = Employee('df', 'f', 'd')
    employee.many_insert()
    print("Выполняется алгоритм 4")


"""
    Замеры скорости выполнения запроса в 5 задании:
    0:00:00.249984 - без индексации колонок name и gender и с использованием name LIKE "F%" 
    0:00:00.108006 - добавление индексов, а также замена LIKE "F%" на поиск по диапозону
    Благодаря индексации мы можем быстрее обращаться к элементам нужных нам столбцов
"""


def algorithm5():
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_employees_name_gender ON employees (name, gender);")
    stmt = '''
        SELECT name, birthday, gender 
        FROM employees
        WHERE gender='Male' AND name >= 'F' AND name < 'G'
    '''
    start_time = datetime.now()
    result = cursor.execute(stmt).fetchall()
    end_time = datetime.now() - start_time
    print(result)
    print(end_time)
    print("Выполняется алгоритм 5")


if __name__ == "__main__":
    if len(sys.argv) != 2 and len(sys.argv) != 5:
        print("Ошибка ввода")
        sys.exit(1)

    algorithm_number = sys.argv[1]

    if algorithm_number == "1":
        algorithm1()
    elif algorithm_number == "2":
        name, birthday, gender = sys.argv[2:5]
        algorithm2(name, birthday, gender)
    elif algorithm_number == "3":
        algorithm3()
    elif algorithm_number == "4":
        algorithm4()
    elif algorithm_number == "5":
        algorithm5()
    else:
        print("Неверный номер алгоритма. Допустимые значения: от 1 до 5")
        sys.exit(1)
    conn.close()
