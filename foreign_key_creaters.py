import hashlib
import json
from mysql.connector import connect, Error


def hash(values):
    return hashlib.md5(str.encode(values)).hexdigest()

def make_alter_query(table, column, ref_table, ref_column):
    hashed = hash(table + column + ref_table + ref_column)
    
    query = ''' 
        ALTER TABLE {}
        ADD FOREIGN KEY
        {} ({})
        REFERENCES {} ({})
    '''.format(table, hashed, column, ref_table, ref_column)

    return query

def read_whole_file(path) {
    file_read = open(path, 'r')
    lines = file_read.
}

if __name__ == '__mail__':
    try:
        with connect(host="localhost", user="root", password="password") as conn:
            cursor = conn.cursor()
            content = read_whole_file('tmp/guess_reference_data.json')
            guessed = json.loads(content)

            
        
            cursor.close()
            conn.close()

    except Error as e:
        print(e)

