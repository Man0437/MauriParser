from person import Person
from modules.fun import validate_birthdate


class Books():

    def __init__(self):
        self.id = 1
    def help(self, conn, args):
        print("""Books module commands:
- help -
- list -
- add -
- edit -
- delete -""")

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

        if args.l:
            filters.append("lastname = %s")
            values.append(args.l)

        if args.d:
            filters.append("divisionid = %s")
            values.append(args.d)

        if args.r:
            filters.append("rank = %s")
            values.append(args.r)

        if args.c:
            filters.append("cadetid = %s")
            values.append(args.c)

        where_clause = ""
        if filters:
            where_clause = "WHERE " + " AND ".join(filters)

        # ---------------- ORDER BY
        order_map = {
            "id": "id",
            "lastName": "lastname"
        }

        order_clause = ""
        if args.s and args.s in order_map:
            order_clause = f"ORDER BY {order_map[args.s]}"

        # ---------------- FINAL QUERY
        query = f"""
            SELECT {select_clause}
            FROM cadet
            {where_clause}
            {order_clause}
        """

        cur.execute(query, values)
        rows = cur.fetchall()

        # ---------------- PRINT
        for row in rows:
            inner = ", ".join(
                f"{field}: {value}"
                for field, value in zip(selected, row)
            )
            print(f"{{Cadet: {{{inner}}}}}")

        cur.close()

    def add(self, conn, args):
        if validate_birthdate(args.b) == False:
            print("Неправильный формат дня рождения")
            return
        
        if args.r != "sergeant" and args.r != "private":
            print("Неправильный ранк для солдата")
            return
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO cadet (
                firstname,
                middlename,
                lastname,
                birthdate,
                rank,
                divisionid
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            args.f,
            args.m,
            args.l,
            args.b,
            args.r,
            args.d
        ))
        conn.commit()
        cur.close()

    def edit(self, conn, args):
        cur = conn.cursor()

        fields = []
        values = []

        if args.f:
            fields.append("firstname = %s")
            values.append(args.f)
        if args.m:
            fields.append("middlename = %s")
            values.append(args.m)
        if args.l:
            fields.append("lastname = %s")
            values.append(args.l)
        if args.b:
            fields.append("birthdate = %s")
            values.append(args.b)
        if args.r:
            fields.append("rank = %s")
            values.append(args.r)
        if args.d:
            fields.append("divisionid = %s")
            values.append(args.d)

        if not fields:
            print("Ничего не передали для обновления")
        values.append(args.i)


        query = f"""
            UPDATE cadet
            SET {', '.join(fields)}
            WHERE id = %s
        """

        cur.execute(query, values)
        conn.commit()
        cur.close
        print("Запись обновлена")

    def delete(self, conn, args):
        cur = conn.cursor()

        if args.a:
            cur.execute("DELETE FROM cadet")
            conn.commit()
            cur.close()
            print(f"Удалены все записи из {args.entity}")
            return


        cur.execute(
            "DELETE FROM cadet WHERE id = %s",
            (args.i,)
        )
        conn.commit()
        cur.close()

        print(f"Удалена запись {args.i} из таблицы {args.entity}")

    def add_help(self):
        print("""Cadet add command parameters:
-f : first name, required
-m : middle name, required
-l : last name, required
-b : birth date, required, format yyyy-MM-dd
-r : rank, required
-d : division ID, required""")

    def list_help(self):
        print("""Cadet list command parameters:
-i : ID
-l : last name
-d : division ID
-r : rank
-o : division officer ID
-s : sorting, possible id, lastName
-p : properties view, combination of i - id, r - rank, f - firstName, m - middleName, l - lastName, b – birthDate""")

    def delete_help(self):
        print("""Cadet delete command parameters:
-i : ID
-d : division ID
-o : division officer ID
-a : delete all cadets""")

    def edit_help(self):
        print("""Cadet edit command parameters:
-i : ID, required
-f : first name
-m : middle name
-l : last name
-b : birth date, format yyyy-MM-dd
-r : rank
-d : division ID""")