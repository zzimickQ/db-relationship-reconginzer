from mysql.connector import connect, Error
from json import dumps
import re
from cli import read_params

from dbs_tables import get_tables

if __name__ == '__main__':
    params = read_params()
    try:
        with connect(host=params.host, user=params.user, password=params.password, port=params.port) as conn:

            tables = get_tables(conn, params.db_prefix)

            cursor = conn.cursor()

            file = open(params.output, 'w')

            for table in tables:
                table_database = table['database']
                table_name = table['name']
                table_columns = table['columns']
                
                file.write('{}.{}\n'.format(table_database, table_name))

            file.close()

            cursor.close()
            conn.close()

    except Error as e:
        print(e)
