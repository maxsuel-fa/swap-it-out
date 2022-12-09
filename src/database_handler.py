import oracledb
import os
from dotenv import load_dotenv

class DatabaseHandler:
    ''' As its name indicates, this class is responsable to handle with 
    all the database operations in the aplication 
    '''
    def __init__(self, authentication_file_path, pool_max=4):
        ''' Initialize the DatabaseHandler class

        Parameters:
            authentication_file -- path for the file that contains the database
                                   login information
            pool_max            -- the maximum size that the pool of connections can 
                                   grow up to
        '''
        # Load the environment variables' file
        load_dotenv(authentication_file_path)

        # Setting the authetication variables
        self.user = os.environ['ORACLEDB_USER']
        self.password = os.environ['ORACLEDB_PASSWORD']
        self.host = os.environ['ORACLEDB_HOST']
        self.port = os.environ['ORACLEDB_PORT']
        self.service_name = os.environ['ORACLEDB_SN']

        # Creating the pool of connections
        # A fixed pool size was used (min=max), as recomended in the 
        # oraclebd library documentation
        self.pool = oracledb.create_pool(user=self.user,
                                         password=self.password,
                                         host=self.host,
                                         port=self.port,
                                         service_name=self.service_name,
                                         min=pool_max,
                                         max=pool_max,
                                         increment=0)

    def insert(self, insert_statement: str, 
               attribute_values: dict):
        ''' Insert a tuple into the table specified in the insert_statement,  
        using the oracledb execute function as base.
        To do so, this method acquires a connection in the connection pool
        created in the class construction and then execute the insert statement
        using such connection
        
        Parameters:
            insert_statement (str)  -- statement to be executed.
                                       In order to avoid SQL injections, it is better to 
                                       pass the statement as a parameter instead of 
                                       creating a statement by biding column and 
                                       table names into a string that represents it. Only 
                                       values bind is made using the library, which prevents
                                       SQLi attacks
            attribute_values (dict) -- the list of the values to be inserted
        '''

        with self.pool.acquire() as connection:
            with connection.cursor() as cursor:
                cursor.execute(insert_statement, attribute_values)
                connection.commit()

    def query(self, query_statement: str,
              condition_values: dict=None) -> list:
        ''' Executes a query in the database

        Parameters:
            query_statement (str)   -- query statement to be executed
            condition_values (dict) -- list of values to be assigned to
                                       each condition declared into the query
                                       statement. 
        
        Return (list) -- all the tuples returned by the query 
        '''
        
        tuples = list()
        with self.pool.acquire() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query_statement, condition_values)
                tuples = cursor.fetchall()
        
        return tuples

    def delete(self, delete_statement: str,
               condition_values: dict):
        ''' Delete a tuple from a table specified in the delete_statement,
        using the oracledb execute function as base. In pratice, this me-
        thod works in the exactly same way as the insert method, but chan-
        ging the name helps the code readability

        Parameters:
            delete_statement (str)  -- statement to be executed
            condition_values (dict) -- list of values to bind to 
                                       the statement
        '''
        self.insert(delete_statement, condition_values)

    def rollback(self):
        ''' The rollback function of the database handler '''
        with self.pool.acquire() as connection:
            connection.rollback 

#db = DatabaseHandler('.env')
#db.insert('insert into project_test (att1, att2) values (:v1, :v2)', [1, 'max'])
#row = db.query('select att1 from project_test where att1=(:val)', [3])
#print(len(row))
