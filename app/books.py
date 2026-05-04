from fun import validate_birthdate
from dataclasses import dataclass

class Books():
    
    def __init__(self):
        self.list_books = []
    
    def help(self, conn, args):
        print("""Books module commands""")

    def list(self, conn, args):
        cur = conn.cursor()

        # ---------------- SELECT (поля)
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

        # ---------------- WHERE (фильтры)
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

        # ---------------- ORDER BY
        order_map = {
            "id": "id",
            "name": "name"
        }

        #order_clause = ""
        #if args.s and args.s in order_map:
        #    order_clause = f"ORDER BY {order_map[args.s]}"

        # ---------------- FINAL QUERY
        query = f"""
            SELECT {select_clause}
            FROM books
            {where_clause}
        """

        cur.execute(query, values)
        rows = cur.fetchall()

        # ---------------- PRINT
        for row in rows:
            inner = ", ".join(
                f"{field}: {value}"
                for field, value in zip(selected, row)
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