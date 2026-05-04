import psycopg2

def conn_dtbs():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="example"
    )
    return conn

# Для теста были сделаны эти функции

def create_dtbs(conn, name_table:str):
    
    cur = conn.cursor()
        
    try:
        if name_table.lower() == "officer":
            cur.execute(f"""
            CREATE TABLE IF NOT EXISTS officer (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                firstname TEXT NOT NULL,
                middlename TEXT NOT NULL,
                lastname TEXT NOT NULL,
                birthdate TEXT NOT NULL,
                rank TEXT NOT NULL,
                divisionid INT,
                created_at TIMESTAMP DEFAULT NOW()
            );
            """)

        elif name_table.lower() == "cadet":
            cur.execute(f"""
            CREATE TABLE IF NOT EXISTS cadet (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                firstname TEXT NOT NULL,
                middlename TEXT NOT NULL,
                lastname TEXT NOT NULL,
                birthdate TEXT NOT NULL,
                rank TEXT NOT NULL,
                divisionid INT,
                created_at TIMESTAMP DEFAULT NOW()
            );
            """)

        elif name_table.lower() == "division":
            cur.execute(f"""
            CREATE TABLE IF NOT EXISTS division (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
            """)

        else:
            print("Введи division, cadet или officer")
            return
        
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()
    
    print(f"Создана таблица {name_table}")
    conn.commit()



def delete_table(conn, name_table):
    cur = conn.cursor()
    cur.execute(f"DROP TABLE IF EXISTS {name_table};")
    conn.commit()
    print(f"Таблица {name_table} удалена")

def sort_dtbs(conn):
    pass