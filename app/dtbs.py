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
        if name_table.lower() == "books":
            cur.execute(f"""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                author TEXT,
                price TEXT,
                money TEXT NOT NULL,        
                created_at TIMESTAMP DEFAULT NOW()
            );
            """)

            print(f"OK | create {name_table.lower()}")

        else:
            print("Введи другое имя")
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