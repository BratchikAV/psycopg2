#!/usr/bin/env python
# coding: utf-8

# In[5]:


import psycopg2
from psycopg2 import Error

try:

    conn = psycopg2.connect(database="clientbase", user="postgres", password="AssAnce_22")

    cur = conn.cursor() 

#создаем таблицы базы данных
    def create_db(conn):
            #удаляем таблицы и содержимое
        cur.execute('''
        DROP TABLE IF EXISTS phone; 
        ''')
        cur.execute('''
        DROP TABLE IF EXISTS client; 
        ''')


        cur.execute('''
        CREATE TABLE IF NOT EXISTS client(
        client_id SERIAL PRIMARY KEY,
        name VARCHAR(40) NOT NULL,
        surname VARCHAR(40) NOT NULL,
        e_mail VARCHAR (60) NOT NULL); 
        ''') 

        cur.execute('''
        CREATE TABLE IF NOT EXISTS phone(
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES client(client_id),
        number INTEGER NOT NULL); 
        ''') 
        print("TABLES has been created successfully !!")
        
        conn.commit()
        pass

 #проверяем наличие клиента в базе
# функция не возвращает  True (False), видимо я забыл всё...
#     def exist(conn, name, surname, e_mail):
#         cur.execute('''
#         SELECT EXISTS (SELECT client_id FROM client WHERE name=%s AND surname=%s AND e_mail=%s);
#         ''', (name, surname, e_mail))
#         exist = cur.fetchone()[0] 
        
#         return exist
    
    
    def add_client(conn):                
        name = input("Enter your name: ")
        surname = input("Enter your surname: ")
        e_mail = input("Enter your e_mail: ")
        cur.execute('''
        SELECT EXISTS (SELECT client_id FROM client WHERE name=%s AND surname=%s AND e_mail=%s);
        ''', (name, surname, e_mail))
        exist = cur.fetchone()[0]
     
        if exist==False:
            cur.execute('''
            INSERT INTO client(name, surname, e_mail)
            VALUES (%s, %s, %s);''', (name, surname, e_mail))
            print("Client was added!")
        else:
            print('This client already exists!')
    
        conn.commit()
        pass
    
    def add_phone(conn):
        name = input("Enter your name: ")
        surname = input("Enter your surname: ")
        e_mail = input("Enter your e_mail: ")
        # проверяем наличие клиента в базе
        cur.execute('''
        SELECT EXISTS (SELECT client_id FROM client WHERE name=%s AND surname=%s AND e_mail=%s);
        ''', (name, surname, e_mail))
        exist = cur.fetchone()[0]
        #eсли такой клиент есть
        if exist==True:
            phone = input("Enter your phone: ")
            cur.execute('''
            SELECT client_id FROM client WHERE name=%s AND surname=%s AND e_mail=%s;
            ''', (name, surname, e_mail))        
            client_id = int(cur.fetchone()[0])
            cur.execute('''
            INSERT INTO phone(client_id, number)
            VALUES (%s, %s);''', (client_id, phone))
            next = input("Add another number? yes OR no? ")
            
            while next == "yes":    
                other_phone = input("Enter your other number: ")
                cur.execute('''
                INSERT INTO phone(client_id, number)
                VALUES (%s, %s);''', (client_id, other_phone))
                next = input("Add another number? yes OR no? ")        
        
#         если такого клиента не существует
        else:
            print('Wrong data! Client is not exist!')
    
        conn.commit()
        pass
    
    # Функция, позволяющая изменить данные о клиенте
    def change_client(conn):
        name = input("Enter  name: ")
        surname = input("Enter  surname: ")
        e_mail = input("Enter  e_mail: ")
        # проверяем наличие клиента в базе
        cur.execute('''
        SELECT EXISTS (SELECT client_id FROM client WHERE name=%s AND surname=%s AND e_mail=%s);
        ''', (name, surname, e_mail))
        exist = cur.fetchone()[0]
        change = input("What do you want to change? name OR surname OR e_mail? ")
        # eсли клиент есть в базе
        if exist==True:
            cur.execute('''
            SELECT client_id FROM client WHERE name=%s AND surname=%s AND e_mail=%s;
            ''', (name, surname, e_mail))        
            client_id = int(cur.fetchone()[0])
            
            if change == "name":
                new_name = input("Write new name: ")
                cur.execute('''
                UPDATE client 
                SET name = %(new_name)s 
                WHERE client_id = %(client_id)s;
                ''', {"new_name": new_name, "client_id": client_id})
            elif change == "surname":
                new_surname = input("Write new surname: ")
                cur.execute('''
                UPDATE client 
                SET surname = %(new_surname)s 
                WHERE client_id = %(client_id)s;
                ''', {"new_surname": new_surname, "client_id": client_id})
            else:
                new_e_mail = input("Write new e_mail: ")
                cur.execute('''
                UPDATE client 
                SET e_mail = %(new_e_mail)s 
                WHERE client_id = %(client_id)s;
                ''', {"new_e_mail": new_e_mail, "client_id": client_id})
        
        
    #         если такого клиента не существует
        else:
            print('Wrong data! Client is not exist!')
    
        conn.commit()    
        pass
    
    
    # Функция, позволяющая удалить телефон для существующего клиента
    def delete_phone(conn):
    # проверка на наличие телефона в базе
        number = int(input("What number do you want to delite? "))
        cur.execute('''
        SELECT EXISTS (SELECT id FROM phone WHERE number=%s);
        ''', (number,))
        exist = cur.fetchone()[0]
        if exist==True:
            # если номер есть в базе
            cur.execute('''
            DELETE FROM phone
            WHERE number = %s;''', (number,))
             #         если такого клиента не существует
        else:
            print('Wrong data! Phone is not exist!')
    
        conn.commit()    
        pass
    
    
    # Функция, позволяющая удалить существующего клиента
    def delete_client(conn):
        name = input("Enter  name: ")
        surname = input("Enter  surname: ")
        e_mail = input("Enter  e_mail: ")
        # проверяем наличие клиента в базе
        cur.execute('''
        SELECT EXISTS (SELECT client_id FROM client WHERE name=%s AND surname=%s AND e_mail=%s);
        ''', (name, surname, e_mail))
        exist = cur.fetchone()[0]
        
        # eсли клиент есть в базе
        if exist==True:
            cur.execute('''
            DELETE FROM client
            WHERE name=%s AND surname=%s AND e_mail=%s);
        ''', (name, surname, e_mail))
        
        #         если такого клиента не существует
        else:
            print('Wrong data! Client is not exist!')
    
        conn.commit()   
        pass
        
        
    # Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону
    def find_client(conn):
        find = input("What do you know about client? name OR surname OR e_mail OR phone? ")
        
        if find=="name":
            name = input("Enter client name: ")
            cur.execute('''
            SELECT * FROM client
            JOIN phone USING (client_id)
            WHERE name=%s;''', (name,))
            client = cur.fetchall()
            print(client)            
        elif find=="surname":
            surname = input("Enter client surname: ")
            cur.execute('''
            SELECT * FROM client
            JOIN phone USING (client_id)
            WHERE surname=%s;''', (surname,))
            client = cur.fetchall()
            print(client)            
        elif find=="e_mail":
            e_mail = input("Enter client e_mail: ")
            cur.execute('''
            SELECT * FROM client
            JOIN phone USING (client_id)
            WHERE e_mail=%s;''', (e_mail,))
            client = cur.fetchall()
            print(client)
        else:
            phone = int(input("Enter client phone: "))
            cur.execute('''
            SELECT * FROM client
            JOIN phone USING (client_id)
            WHERE number=%s;''', (phone,))
            client = cur.fetchall()
            print(client)
            
            conn.commit()
        pass
#         
    
    create_db(conn)
   
    add_client(conn)
    add_client(conn)
    cur.execute('''
    SELECT * FROM client;
    ''')        
    id = cur.fetchone()
    print(id)
    
    add_phone(conn)
    cur.execute('''
    SELECT * FROM phone;
    ''')        
    id = cur.fetchone()
    print(id)
    
    change_client(conn)      
    cur.execute('''
    SELECT * FROM client;
    ''')        
    id = cur.fetchone()
    print(id)

    delete_phone(conn)
    cur.execute('''
    SELECT * FROM phone;
    ''')        
    id = cur.fetchall()
    print(id)
    find_client(conn)
    find_client(conn)




except (Exception, Error) as error:
    print("Ошибка в PostgreSQL", error)
finally:
    if conn:
        cur.close()
        conn.close()
        print("Connection is closed!")



# In[20]:





# In[ ]:







# In[ ]:




