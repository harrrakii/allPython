import sqlite3


class Base:
    def __init__(self):
        self.conn = sqlite3.connect("salon.sqlite")
        self.cur = self.conn.cursor()
        self.adder()

    def action(self, query, values):
        try:
            with self.conn:
                self.cur.execute(query, values)
        except Exception as e:
            pass

    def update_data(self, table: str, data: dict, params: dict):
        columns = ', '.join(f"{value} = ?" for value in data.keys())
        parametr = ", ".join(f"{param} = ?" for param in params.keys())
        values = list(data.values()) + list(params.values())
        query = f"UPDATE {table} SET {columns} WHERE {parametr}"
        self.action(query, values)

    def insert(self, table: str, data: dict):
        columns = ", ".join(f"{key}" for key in data.keys())
        none = ", ".join("?" for _ in data.keys())
        query = f"INSERT INTO {table} ({columns}) VALUES({none})"
        self.action(query, list(data.values()))

    def delete(self, table: str, params: dict):
        columns = ", ".join("?" for _ in params.keys())
        query = f"DELETE FROM {table} WHERE {columns}"
        self.action(query, list(params.values()))

    def read(self, table: str, columns: list, params=None, all=None):
        try:
            values = []
            data = ", ".join(columns)
            query = f"SELECT {data} FROM {table}"
            with self.conn:
                if params:
                    param = " and ".join(f"{parametr} = ?" for parametr in params.keys())
                    query = f"SELECT {data} FROM {table} WHERE {param}"
                    values = list(params.values())
                if all:
                    return self.cur.execute(query, values).fetchall()
                else:
                    return self.cur.execute(query, values).fetchone()
        except Exception:
            pass

    def adder(self):
        script = """
        create table if not exists users(
            id integer primary key autoincrement,
            login varchar(20) unique,
            password varchar(20)
        );
        create table if not exists salons(
            id integer primary key autoincrement,
            title varchar(20) unique,
            address text
        );
        create table if not exists employees(
            id integer primary key autoincrement,
            login varchar(20) unique,
            password varchar(20),
            name text,
            price integer,
            experience integer
        );
        create table if not exists records(
            id integer primary key autoincrement, 
            user_id integer,
            employee_id integer,
            salon_id integer,
            price integer,
            record_date date,
            confirmation boolean,
            foreign key (user_id) references users(id),
            foreign key (employee_id) references employees(id),
            foreign key (salon_id) references salons(id)
        );
        """
        salons = [[1, "prasta", "Москва, ул. Гурьева 73"], [2, "Coulet", "Москва, ул. Алексндрова 1б"],
                  [3, "Ghiely", "Москва ул. Воронцовская 53 с1/2"]]
        query_salons = "INSERT INTO salons VALUES(?, ?, ?)"
        employees = [[1, "a", "a", "a", 1500, 4], [2, "b", "b", "b", 1000, 2],
                     [3, "c", "c", "c", 2300, 0]]
        query_employees = "INSERT INTO employees VALUES(?, ?, ?, ?, ?, ?)"
        try:
            with self.conn:
                self.cur.executescript(script)
                self.cur.executemany(query_employees, employees)
                self.cur.executemany(query_salons, salons)
        except Exception as e:
            pass








