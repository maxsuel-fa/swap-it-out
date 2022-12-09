from database_handler import DatabaseHandler
import constants as const
import application_backend as app_backend
import application_frontend as app_frontend
import constants as const
#db = DatabaseHandler('.env')
#app_backend.register_collector([0], db)


if __name__ == '__main__':
    db_handler = DatabaseHandler('.env')
    option = 0
    while option != const.SAIR:
        if not option:
            app_frontend.options_screen()
            option = int(input('Escolha uma das opcoes acima: '))
        elif option == 1:
            app_frontend.register_collector_screen()
            validation_num = app_backend.register_collector(db_handler)

            if validation_num == const.SUCCESS:
                app_frontend.register_collector_success_screen()
                option = 0
            elif validation_num == const.COLLECTOR_USERNAME_ERROR:
                app_frontend.error_username_screen()
            elif validation_num == const.COLLECTOR_CPF_ERROR:
                app_frontend.error_cpf_screen()
            else:
                print('erro')
                #general_error_screen()

