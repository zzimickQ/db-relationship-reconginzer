import argparse

_parser = argparse.ArgumentParser(description='Predictive MySQL column relationship recongnizer.')

_parser.add_argument('--db-prefix', '-d',  
                            required=True,
                            type=str, 
                            help='prefix of the databases that will be considered in the database')

_parser.add_argument('--output', '-o',     
                            required=True,
                            default='./guess_data.json', 
                            type=str, 
                            help='the output file for the predicted relationships')

_parser.add_argument('--host',       
                            default='localhost', 
                            type=str, 
                            help='database host')

_parser.add_argument('--port', '-p',       
                            default=3306, 
                            type=int, 
                            help='database port')

_parser.add_argument('--user', '-u',       
                            default='root', 
                            type=str, 
                            help='database user')

_parser.add_argument('--password', '-s',   
                            default='password', 
                            type=str, 
                            help='database password')



params = _parser.parse_args()

if __name__ == '__main__':
    print(params)