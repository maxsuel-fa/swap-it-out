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



    # First, register the user as a person in the database
    try:
        sql_statement_person = ''' insert into pessoa
                                   values (:username,
                                           :CPF,
                                           :nome,
                                           to_date(:data_nascimento, :format),
                                           :CEP,
                                           :numero,
                                               :cidade,
                                           :rua) '''
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

    
    # Then, register the collector
    try:
        sql_statement_coll = ''' insert into colecionador
                                 values (:username)'''
        db_handler.insert(sql_statement_coll,
                          dict(username = collector_data['username']))
    except:
        # If occours an error in registering the colector
        # undo the person registration
        db_handler.rollback()
        sql_statement_del = ''' delete from pessoa 
                                where username = (:username) '''
        db_handler.delete(sql_statement_del,
                          dict(username = collector_data['username']))
        return const.ERROR

    # At last, register the function
    try:
        sql_statement = ''' insert into funcao
                            values (:username, :funcao)
                        '''
        db_handler.insert(sql_statement, 
                          dict(username = collector_data['username'],
                               funcao = 'COLECIONADOR'))
    except:
        # If occours an error in registering the functio
        # undo the person and collector registration
        db_handler.rollback()
        sql_statement_del = ''' delete from colecionador 
                                where username = (:username) '''
        db_handler.delete(sql_statement_del,
                          dict(username = collector_data['username']))

        sql_statement_del = ''' delete from pessoa 
                                where username = (:username) '''
        db_handler.delete(sql_statement_del,
                          dict(username = collector_data['username']))
        return const.ERROR

    return const.SUCCESS


def collector_statistics(db_handler: DatabaseHandler):
    ''' Calculates the percentage of completion of
    all albums for a user

    Parameters:
        db_handler (DatabaseHandler) -- object to handle database operations

    Return (int) -- the constant SUCCESS if the registration goes well,
                    or another constant indicating the specific error
    '''

    condition_values = dict()

    username = input('Entre com o username do colecionador: ')

    # Checking if there is a user with the entered username
    # in the database

    sql_statement = '''select username
                            from colecionador
                            where username = (:un)'''

    has_user = len(db_handler.query(sql_statement,
                                    dict(un = username)))

    if has_user:
        sql_statement = '''select f.id_album, a.colecao, count(*)
                           from figurinha f join album_colecionador ac
                               on ac.id_album = f.id_album
                               and ac.username = (:un)
                               join album a
                                   on a.id_album = f.id_album
                           where (f.cod_figurinha, f.tipo, f.id_album) not in
                               (select fig.cod_figurinha, fig.tipo, fig.id_album
                                from figurinha_colecionador fc join figurinha fig
                                    on fc.cod_figurinha = fig.cod_figurinha
                                    and fc.id_album = fig.id_album
                                where fc.username = (:un))
                           group by f.id_album, a.colecao
        '''
        collector_albums_stat = db_handler.query(sql_statement,
                                                 dict(un = username))
        sql_statement = ''' select f.id_album, count(*)
                            from figurinha f
                            group by f.id_album
        '''
        general_stat = db_handler.query(sql_statement)

        stats = dict()

        for (id_album1, album_name, x)  in collector_albums_stat:
            for (id_album2, y) in general_stat:
                if id_album1 == id_album2:
                    percent = 100 - (x/y) * 100
                    stats[album_name] = percent
        return stats

    else:
        return const.ERROR_USER_NOT_FOUND




