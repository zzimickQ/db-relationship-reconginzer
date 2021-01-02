from mysql.connector import connect, Error
from json import dumps
import re

if __name__ == '__main__':

    try:
        with connect(host="localhost", user="root", password="password") as conn:

            # repeated column defenitions
            to_table_col_name = 'candidate_table'
            relation_column = 'found_in_tables'
            candidate_level_col = 'candidate_level'
            is_dangling_col = 'is_dangling'
            
            # all table names with their respected database prepended
            # will be put here
            all_tables = []

            # referencing columns will be put to a dict
            reference_count_per_match = {}

            # initialized mysql cursor
            cursor = conn.cursor()
            
            # get databases
            cursor.execute('SHOW DATABASES')
            databases = cursor.fetchall()

            # filter jungoo databases
            jugnoo_databases = filter(lambda x: 'jugnoo_' in x[0], databases)
            

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

                    # construct full table name
                    full_table_name = '{}.{}'.format(database_name,table_name)

                    # get table details
                    cursor.execute('DESCRIBE `{}`'.format(table_name))
                    columns = cursor.fetchall()

                    # make table model
                    table_model = {'name': full_table_name, 'columns': columns}

                    # collect tables with thier respective database
                    all_tables.append(table_model)

                    for column in columns:
                        # get column name
                        column_name = column[0]

                        # check if a _id is in the column name to identify 
                        # if it's a referencing column
                        if '_id' in column_name:

                            #check if the column name is in the refering list
                            if column_name in reference_count_per_match.keys():
                                # if so append another table to the referencing column
                                reference_count_per_match[column_name][relation_column].append(full_table_name)
                            else:
                                # if not create a column for that purpose and provide it a table name
                                reference_count_per_match[column_name] = {relation_column: [], to_table_col_name: []}


            # sort the references with significance of referenced table count
            # this process removed the dict and changes it to a tuple
            reference_count_per_match = sorted(reference_count_per_match.items(), key=lambda x: len(x[1][relation_column]), reverse=True)

            # create a dict to map the references back to 
            # thier original size
            reference_count_per_match_obj = {}

            # loop over the sorted list and
            # map it back to the original dict structure
            for item in reference_count_per_match:
                reference_count_per_match_obj[item[0]] = item[1]
                reference_count_per_match_obj[item[0]]['count'] = len(item[1][relation_column])

            # map all table names
            all_table_names = []
            all_table_names_str = ''
            for table in all_tables:
                all_table_names.append(table['name'])
                all_table_names_str += table['name'] + '\n'
            
            # loop through referncing columns
            # to find their candidate table
            for reference_column in reference_count_per_match_obj.keys():

                
                # remove the _id and anything after it from the reference columns
                reference_as_table = re.sub(r'(_id.*)$', '', reference_column)


                # if final str ends with a 'y' remove the character
                if reference_as_table[-1] == 'y':
                    reference_as_table = reference_as_table[:-1]

                # do a specific search where it will search for tb_ at front and 
                # and ies or s or two letters in the end and ends with that letter
                match = re.compile(r'^(.*\.tb_{}(ies|s|..))$'.format(reference_as_table), re.M | re.A)

                reference_count_per_match_obj[reference_column][to_table_col_name] = match.findall(all_table_names_str)

                if len(reference_count_per_match_obj[reference_column][to_table_col_name]) > 0:
                    # tag the candidate level as high
                    reference_count_per_match_obj[reference_column][candidate_level_col] = 'HIGH_CANDIDATE'

                if len(reference_count_per_match_obj[reference_column][to_table_col_name]) == 0:
                    match = re.compile(r'^(.*\.{}.*)$'.format(reference_as_table))
                    reference_count_per_match_obj[reference_column][to_table_col_name] = match.findall(all_table_names_str)
                    reference_count_per_match_obj[reference_column][candidate_level_col] = 'MEDIUM_CANDIDATE'

                if len(reference_count_per_match_obj[reference_column][to_table_col_name]) == 0:
                    match = re.compile(r'(.*{}.*)'.format(reference_as_table))
                    reference_count_per_match_obj[reference_column][to_table_col_name] = match.findall(all_table_names_str)
                    reference_count_per_match_obj[reference_column][candidate_level_col] = 'LOW_CANDIDATE'
                
                if len(reference_count_per_match_obj[reference_column][to_table_col_name]) == 0:
                    reference_count_per_match_obj[reference_column][candidate_level_col] = 'NO_CANDIDATE'

                reference_count_per_match_obj[reference_column][to_table_col_name] = list(reference_count_per_match_obj[reference_column][to_table_col_name])

                # # loop through all tables and match 
                # for table in all_table_names:
    

                #     if match.match(table):
                #         # tag the candidate level as high
                #         reference_count_per_match_obj[reference_column][candidate_level_col] = 'HIGH_CANDIDATE'

                
                #     # if no candidate tables were not found for this ref column
                #     if len(reference_count_per_match_obj[reference_column][to_table_col_name]) == 0:
                    
                #         # loop through all tables and match 
                #         for table in all_table_names:

                #             # do another match with the ref column but only tb_ is required in the front
                #             match = re.compile(r'(.*\.tb_{}.*)'.format(reference_as_table))

                #             if match.match(table):
                #                 reference_count_per_match_obj[reference_column][to_table_col_name].append(table)
                #                 # tag the candidate level as medium
                #                 reference_count_per_match_obj[reference_column][candidate_level_col] = 'MEDIUM_CANDIDATE'

                    
                #     # if no candidate tables were not found for this ref column
                #     if len(reference_count_per_match_obj[reference_column][to_table_col_name]) == 0:
                    
                #         # loop through all tables and match 
                #         for table in all_table_names:
                        
                #             # do another match with the ref column that contains the name
                #             match = re.compile(r'(.*{}.*)'.format(reference_as_table))
                            
                #             if match.match(table):
                #                 reference_count_per_match_obj[reference_column][to_table_col_name].append(table)
                #                 # tag the candidate level as low
                #                 reference_count_per_match_obj[reference_column][candidate_level_col] = 'LOW_CANDIDATE'


                #     # if no candidate tables were not found for this ref column
                #     if len(reference_count_per_match_obj[reference_column][to_table_col_name]) == 0:
                #         # tag the candidate level as no candidates
                #         reference_count_per_match_obj[reference_column][candidate_level_col] = 'NO_CANDIDATE'
                #         # show if a column both doesn't have a candidate table and has no references
                #         reference_count_per_match_obj[reference_column][is_dangling_col] = reference_count_per_match_obj[item[0]]['count'] == 0


            # dump collected data to json
            json_print = dumps(reference_count_per_match_obj, indent=4)

            # save dump to file
            open('tmp/guess_reference_data.json', 'w').write(json_print)


            # close table connections because we no longer query the database
            cursor.close()
            conn.close()
    except Error as e:
        print(e)