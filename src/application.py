from database_handler import DatabaseHandler
import constants as const
import application_backend as app_backend
import application_frontend as app_frontend
import constants as const

if __name__ == '__main__':
    db_handler = DatabaseHandler('.env')
    option = 0
    while option != const.QUIT:
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
        elif option == 2:
            get_stats = app_backend.collector_statistics(db_handler)
            if isinstance(get_stats, dict):
                app_frontend.print_collector_stats(get_stats)
                option = 0
            else:
                app_frontend.user_not_found_screen()
        if option == const.QUIT:
            app_frontend.close_application_screen()


