import oracledb
import constants as const
from database_handler import DatabaseHandler

def register_collector(db_handler: DatabaseHandler) -> int:
    ''' Given all the information data
    that describes a new collector, this function regis-
    ter him in the database of the application

    Parameters:
        db_handler (DatabaseHandler) -- object to handle database operations

    Return (int) -- the constant SUCCESS if the registration goes well, 
                    or another constant indicating the specific error.
                    For instance, if the user name is already registered,
                    this function will return the COLLECTOR_USERNAME_ERROR
                    constant
    '''

    attributes = ['username', 'CPF', 'nome', 'data_nascimento',
                  'CEP', 'numero', 'cidade', 'rua']

    # List to store the collector data
    collector_data = dict()
    input_data = 0
    for attr in attributes:
        if attr == 'data_nascimento':
            input_data = input(f'Entre com a {attr} no formato dd/mm/yyyy: ')
            collector_data['format'] = 'dd/mm/yyyy'
        elif attr == 'Numero':
            input_data = int(input(f'Entre com {attr}: '))
        else:
            input_data = input(f'Entre com {attr}: ')
        collector_data[attr] = input_data

    sql_statement_person = ''' insert into pessoa
                                   values (:username,
                                           :CPF,
                                           :nome,
                                           to_date(:data_nascimento, :format),
                                           :CEP,
                                           :numero,
                                           :cidade,
                                           :rua) '''
    
    # First, register the user as a person in the database                                
    try:
        db_handler.insert(sql_statement_person, collector_data)
    except oracledb.IntegrityError as error:
        db_handler.rollback()
        error, = error.args
        constraints = dict (
            PK_PESSOA = const.COLLECTOR_USERNAME_ERROR,
            UNI1_PESSOA = const.COLLECTOR_CPF_ERROR
        )

        for ct in constraints:
            if(str(error.message).find(ct) >= 0):
                return constraints[ct]
    except Exception:
        db_handler.rollback()
        return const.ERROR

    sql_statement_coll = ''' insert into colecionador
                                 values (:username)'''
    # Then, register the collector
    try:
        db_handler.insert(sql_statement_coll, 
                          dict(username = collector_data['username']))
    except:
        # If occours an error in registering the colector
        # undo the person registration
        db_handler.rollback()
        db_handler.delete(sql_statement_del, 
                          dict(username = collector_data['username']))
        return const.ERROR

    return const.SUCCESS

def register_album(db_handler: DatabaseHandler) -> int:
    ''' Given all the information data
    that describes an album, this function regis-
    ters it in the database of the application

    Parameters:
        db_handler (DatabaseHandler) -- object to handle database operations

    Return (int) -- the constant SUCCESS if the registration goes well, 
                    or another constant indicating the specific error.
    '''
    pass

def register_sticker_available(db_handler: DatabaseHandler) -> int:
    ''' Given all the informations about a sticker and its owner,
    register it as a sticker availabe to swap out

    Parameters:
        db_handler (DatabaseHandler) -- object to handle database operations

    Return (int) -- the constant SUCCESS if the registration goes well, 
                    or another constant indicating the specific error
    '''
    return 
    sticker_data = dict()

    input_data = input('Entre com seu nome de usuario: ')
    sticker_data['username'] = input_data

    input_data = input('Entre com o codigo mostrado na figurinha que deseja cadastrar: ')
    sticker_data['cod_figurinha'] = input_data

    input_data = int(input('Entre com a quantidade de figurinhas do mesmo tipo: '))
    sticker_data['quant'] = input_data

    input_data = input('Entre com o nome do album: ')
    
    # Searching for the album with the given name
    sql_statement_album = ''' select id_album
                              from album
                              where coleacao = (:nome_album)'''
    album = db_handler.query(sql_statement_album, 
                             dict(nome_album = input_data))

    
