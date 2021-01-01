from mysql.connector import connect, Error
from json import dumps
import re

from dbs_tables import get_tables

if __name__ == '__main__':
    try:
        with connect(host="localhost", user="root", password="password") as conn:

            tables = get_tables(conn, "jugnoo_")

            cursor = conn.cursor()

            for table in tables:
                table_database = table['database']
                table_name = table['name']
                table_columns = table['columns']
                print('{}.{}'.format(table_database, table_name))
                try:
                    cursor.execute('USE `{}`'.format(table_database))
                    cursor.execute('TRUNCATE `{}`'.format(table_name))
                except Error as e:
                    print(e)

            cursor.close()
            conn.close()

    except Error as e:
        print(e)
