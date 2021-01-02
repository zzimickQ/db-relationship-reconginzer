from mysql.connector import connect, Error
from json import dumps
import re

def get_tables(conn, db_prefix):
     
    all_tables = []

    # initialized mysql cursor
    cursor = conn.cursor()
    
    # get databases
    cursor.execute('SHOW DATABASES')
    databases = cursor.fetchall()

    # filter jungoo databases
    jugnoo_databases = filter(lambda x: db_prefix in x[0], databases)
    
    for database in jugnoo_databases:
        # get database name
        database_name = database[0]
        
        # switch database
        cursor.execute('USE `{}`'.format(database_name))

        # get tables
        cursor.execute('SHOW TABLES')
        tables = cursor.fetchall()


        for table in tables:
            # get table name
            table_name = table[0]

            # get table details
            cursor.execute('DESCRIBE `{}`'.format(table_name))
            columns = cursor.fetchall()

            cursor.execute('SHOW KEYS FROM `{}` WHERE Key_name = \'PRIMARY\''.format(table_name))
            primary_keys = cursor.fetchall()
            primary_key = None

            if len(primary_keys) > 0:
                if len(primary_keys[0]) > 5:
                    primary_key = primary_keys[0][4]
            
            # map columns to their names only 
            columns = list(map(lambda col: col[0], columns))

            # make table model
            table_model = {
                'database': database_name, 
                'name': table_name, 
                'full_name': '{}.{}'.format(database_name, table_name),
                'columns': columns, 
                'primary': primary_key
                }

            # collect tables with thier respective database
            all_tables.append(table_model)

    cursor.close()
    return all_tables


if __name__ == '__main__':

    
    try:
        with connect(host="localhost", user="root", password="password") as conn:

            all_tables = get_tables(conn, 'jugnoo_')
            for table in all_tables:
                pass
                print('table {}\' primary key is {}'.format(table['name'].ljust(50), table['primary']))

    except Error as error:
        print(error)