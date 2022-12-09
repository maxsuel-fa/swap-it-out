import oracledb
import constants as const
from database_handler import DatabaseHandler 

def register_collector(db_handler: DatabaseHandler) -> int:
    ''' Given a list cotaining all the information data 
    that describes a new collector, this function regis-
    ter him in the database of the application

    Parameters:
        collector_data (list)        -- informations, such as chosen username, 
                          CPF, about the new collector
        db_handler (DatabaseHandler) -- object to handle database operations

    Return (int) -- 1 if the user was successfuly registrated. 0 otherwise
    '''

    attributes = ['username', 'CPF', 'nome', 'data de nascimento', 
                  'CEP', 'numero', 'cidade']

    # List to store the collector data
    collector_data = list()

    for attr in attributes:
        if attr == 'data de nascimento':
            input_data = input(f'Entre com a {attr} no formato mm/dd/yy: ')
        elif attr == 'Numero':
            input_data = int(input(f'Entre com {attr}: '))
        else:
            input_data = input(f'Entre com {attr}: ')
        collector_data.append(input_data)


    sql_statement = ''' insert into pessoa values (username, 
                                            cpf, 
                                            nome, 
                                            to_date(data_nascimento), 
                                            CEP,
                                            numero,
                                            cidade) '''

    try:
        db_handler.insert(sql_statement, collector_data)
    except oracledb.IntegrityError as error:
        error_args = error.args

        constraints = dict (
            PK_PESSOA = const.COLLECTOR_USERNAME_ERROR,
            UNI1_PESSOA = const.COLLECTOR_CPF_ERROR
        )

        for ct in constraints:
            if(str(error_args.message).find(ct) >= 0):
                return constraint[ct]
    except Exception:
        return const.COLLECTOR_CPF_ERROR

    return const.SUCCESS


