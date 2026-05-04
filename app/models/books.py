from fun import validate_birthdate
from dataclasses import dataclass

import logging
from logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

def make_execute_list(args):
        field_map = {
            "i": "id",
            "n": "name",
            "a": "author",
            "t": "type",
            "p": "price" 
        }
        if args.p:
            selected = [field_map[ch] for ch in args.p if ch in field_map]
        else:
            selected = list(field_map.values())
        select_clause = ", ".join(selected)
        filters = []
        values = []
        if args.i:
            filters.append("id = %s")
            values.append(args.i)

        if args.n:
            filters.append("name = %s")
            values.append(args.n)

        if args.t:
            filters.append("type = %s")
            values.append(args.t)

        if args.a:
            filters.append("author = %s")
            values.append(args.a)

        if args.p:
            filters.append("price = %s")
            values.append(args.p)

        if args.m:
            filters.append("money = %s")
            values.append(args.m)

        where_clause = ""
        if filters:
            where_clause = "WHERE " + " AND ".join(filters)
        order_map = {
            "id": "id",
            "name": "name"
        }
        query = f"""
            SELECT {select_clause}
            FROM books
            {where_clause}
        """
        return (query, values, selected)

class Books():
    def __init__(self):
        self.list_books = []

class BookRepository():
    def __init__(self):
        self.books = []
    
    def help(self, conn, args):
        print("""Books module commands""")

    def list(self, conn, args):
        cur = conn.cursor()
        query_values_selected = make_execute_list(args)
        cur.execute(query_values_selected[0], query_values_selected[1])
        rows = cur.fetchall()

        # Вывод в консоль
        for row in rows:
            inner = ", ".join(
                f"{field}: {value}"
                for field, value in zip(query_values_selected[2], row)
            )
            print(f"{{Books: {{{inner}}}}}")

        cur.close()

    def add(self, conn, args): # Здесь args - это список с кортежами значений из htmlparse!
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO books (
                name,
                type,
                author,
                price,
                money
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            args[0],
            args[1],
            args[2],
            args[3],
            args[4]
        ))
        conn.commit()
        cur.close()

# Возможно будет удаление

    def delete(self, conn, args):
        cur = conn.cursor()

        if args.a:
            cur.execute("DELETE FROM books")
            conn.commit()
            cur.close()
            print(f"Удалены все записи из {args.entity}")
            return


        cur.execute(
            "DELETE FROM books WHERE id = %s",
            (args.i,)
        )
        conn.commit()
        cur.close()

        print(f"Удалена запись {args.i} из таблицы {args.entity}")