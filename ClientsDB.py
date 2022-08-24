import psycopg2

conn = psycopg2.connect(database="ClientBase_db", user="postgres", password="пароль")
with conn.cursor() as cur:

    def del_tables(cur):
        cur.execute("""
        DROP TABLE phones;
        """)
        cur.execute("""
        DROP TABLE clients;
        """)
        conn.commit()
#    del_tables(cur)

    def create_db(cur):
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
        id INTEGER PRIMARY KEY UNIQUE,
        name VARCHAR(20) NOT NULL,
        surename VARCHAR(20) NOT NULL,
        email VARCHAR(30) NOT NULL UNIQUE
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES clients (id)
        ON DELETE CASCADE,
        phone VARCHAR(15) DEFAULT NULL
        );
        """)
        conn.commit()
#    create_db(cur)

    def add_client(cur,cl_id, first_name, last_name, e_mail,phone_num=None):

        cur.execute(f"""
        INSERT INTO clients(id,name,surename,email)
        VALUES('{cl_id}','{first_name}','{last_name}','{e_mail}')
        RETURNING id,name,surename,email;
        """)
        print(cur.fetchone())

        cur.execute(f"""
        INSERT INTO phones(client_id,phone)
        VALUES('{cl_id}','{phone_num}')
        RETURNING client_id,phone;
        """)
        print(cur.fetchone())
        conn.commit()
#    add_client(cur,1,'Jhon','Travolta','Tarantino@mail.ru',89117778899)
#    add_client(cur,2,'Jakie','Chan','Fat@mail.ru',89113336655)
#    add_client(cur,3,'Marry','Popins','Nice@mail.ru')

    def add_phone(cur, cl_id, phone_num = None):
        cur.execute(f"""
        INSERT INTO phones(client_id,phone)
        VALUES('{cl_id}','{phone_num}')
        RETURNING client_id,phone;
        """)
        print(cur.fetchone())
        conn.commit()
#    add_phone(cur, 3, 89214448866)
#    add_phone(cur, 2, 81112223344)


    def change_client(cur, cl_id, first_name, last_name, e_mail, phone_num=None):
         cur.execute(f"""
         UPDATE clients
         SET name = '{first_name}', surename = '{last_name}', email = '{e_mail}'
         WHERE id = '{cl_id}'
         RETURNING id, name, surename, email;
         """)
         print(cur.fetchall())

         cur.execute(f"""
         UPDATE phones
         SET phone = '{phone_num}'
         WHERE client_id = '{cl_id}'
         RETURNING client_id, phones;
         """)
         print(cur.fetchall())
         conn.commit()
#    change_client(cur, 1, 'Jhon', 'Travolta' , 'Tarantino@mail.ru', 89117778899)

    def delete_phone(cur, cl_id, phone_num):
        cur.execute(f"""
        DELETE FROM phones
        WHERE client_id = '{cl_id}' AND phone='{phone_num}'
        RETURNING 'ALL OK';
        """)
        print(cur.fetchall())
        conn.commit()
#    delete_phone(cur, 3, 89214448866)


    def delete_client(cur, cl_id):
        cur.execute(f"""
        DELETE FROM clients
        WHERE id = '{cl_id}'
        RETURNING 'ALL OK';
        """)
        print(cur.fetchall())
        conn.commit()
#    delete_client(cur, 3)

    def find_client(cur, first_name=None, last_name=None, e_mail=None, phone_num=None):
        cur.execute(f"""
        SELECT clients.name, clients.surename, clients.email, phones.phone FROM clients
        JOIN phones ON clients.id = phones.client_id
        WHERE name LIKE '%{first_name}%' OR surename LIKE '%{last_name}%'
        OR email LIKE '%{e_mail}%' OR phone LIKE '%{phone_num}%'
        GROUP BY clients.name, clients.surename, clients.email, phones.phone;
        """)
        print(cur.fetchall())
#    find_client(cur, first_name='Marry', last_name=None, e_mail=None, phone_num=None)

    def all_data(cur):
        cur.execute(f"""
        SELECT * FROM clients;
        """)
        print(cur.fetchall())

        cur.execute(f"""
        SELECT client_id,phone FROM phones;
        """)
        print(cur.fetchall())
#    all_data(cur)

conn.close()
