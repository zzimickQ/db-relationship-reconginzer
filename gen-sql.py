import hashlib
import json
from dbs_tables import get_tables
from mysql.connector import connect, Error


def hash(values):
    return hashlib.md5(str.encode(values)).hexdigest()

def make_alter_query(table, column, ref_table, ref_column):
    hashed = 'ref_' + hash(table + column + ref_table + ref_column)
    
    query = ''' 
    ALTER TABLE {}
    ADD FOREIGN KEY
    {} ({})
    REFERENCES {} ({});
    '''.format(table, hashed, column, ref_table, ref_column)

    return query

def read_whole_file(path):
    file_read = open(path, 'r')
    data = '\n'.join(file_read.readlines())
    file_read.close()
    return data


def _clean_array_to_string(arr_or_string):
    if type(arr_or_string) is list:
        return arr_or_string[0]
    return arr_or_string

def clean_array(arr_list):
    return list(map(_clean_array_to_string, arr_list))

if __name__ == '__main__':
    try:
        with connect(host="localhost", user="root", password="password") as conn:

            sql_file = open('alter_relasions.sql', 'w')

            cursor = conn.cursor()
            content = read_whole_file('tmp/guess_reference_data.json')
            guessed = json.loads(content)
            
            all_tables = get_tables(conn, 'jugnoo_')

            all_tables_full_name_keyed = {}

            for table in all_tables:
                all_tables_full_name_keyed[table['full_name']] = table

            for column in guessed.keys():
                data = guessed[column]
                found_in_tables = data['found_in_tables']
                candidate_tables = data['candidate_table']
                level = data['candidate_level']

                if level != "HIGH_CANDIDATE":
                    continue

                candidate_tables = clean_array(candidate_tables)

                for candidate_table in candidate_tables:
                    table = all_tables_full_name_keyed[candidate_table]
                    primary_key = table['primary']

                    for referencing_table in found_in_tables:
                        sql_file.write(
                            make_alter_query(candidate_table, primary_key, referencing_table, column)
                        )



            print("Done!")

        
            cursor.close()
            conn.close()

    except Error as e:
        print(e)

