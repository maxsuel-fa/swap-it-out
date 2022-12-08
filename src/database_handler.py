import oracledb
import os
from os.path import join
from dotenv import load_dotenv

class DatabaseHandler:
    ''' As its name indicates, this class is responsable to handle with 
    all the database operations in the aplication 
    '''
    def __init__(self, authentication_file_path):
        ''' Initialize the DatabaseHandler class

        Parameters:
            authentication_file -- path for the file that contains the database
                                   login information
        '''
        # Load the environment variables' file
        load_dotenv(authentication_file_path)

        self.user = os.environ['ORACLEDB_USER']
        self.password = os.environ['ORACLEDB_PASSWORD']
        self.host = os.environ['ORACLEDB_HOST']
        self.port = os.environ['ORACLEDB_PORT']
        self.service_name = os.environ['ORACLEDB_SN']


