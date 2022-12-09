import os
from time import sleep

def clear_screen():
    ''' Clears the screen acording to the operational system '''
    os_name = dict(
        posix = 'clear',
        nt    = 'cls'
    )
    os.system(os_name[os.name])


def options_screen():
    ''' Draw the options into the terminal '''

    clear_screen()
    print('\t\t\t\t+------------------------------------------------------------+')
    print('\t\t\t\t|            GERENCIADOR DE TROCAS DE FIGURINHAS             |')
    print('\t\t\t\t+------------------------------------------------------------+')
    print('\t\t\t\t|                           OPCOES                           |')
    print('\t\t\t\t|                                                            |')
    print('\t\t\t\t| 1) CADASTRAR COLECIONADOR                                  |')
    print('\t\t\t\t|                                                            |')
    print('\t\t\t\t| 2) BUSCAR PORCENTAGEM COMPLETA DO ALBUM PARA UM            |')
    print('\t\t\t\t|    COLECIONADOR                                            |')
    print('\t\t\t\t|                                                            |')
    print('\t\t\t\t| 3) REGISTRAR TROCA                                         |')
    print('\t\t\t\t|                                                            |')
    print('\t\t\t\t| 4) SAIR DA APLICACAO                                       |')
    print('\t\t\t\t+------------------------------------------------------------+')


def error_username_screen():
    clear_screen()
    print('\t\t\t\t+----------------------------------------------------------------------+')
    print('\t\t\t\t|                                                                      |')
    print('\t\t\t\t|     ERRO AO REGISTRAR COLECIONADOR: NOME DE USUARIO JA UTILIZADO     |')
    print('\t\t\t\t|                                                                      |')
    print('\t\t\t\t+----------------------------------------------------------------------+')
    sleep(5)


def error_cpf_screen():
    clear_screen()
    print('\t\t\t\t+------------------------------------------------------+')
    print('\t\t\t\t|                                                      |')
    print('\t\t\t\t|     ERRO AO REGISTRAR USUARIO: CPF JA CADASTRADO     |')
    print('\t\t\t\t|                                                      |')
    print('\t\t\t\t+------------------------------------------------------+')
    sleep(5)

def register_collector_screen():
    clear_screen()
    print('\t\t\t\t+------------------------------------------------------+')
    print('\t\t\t\t|                                                      |')
    print('\t\t\t\t|                REGISTRO DE COLECIONADOR              |')
    print('\t\t\t\t|                                                      |')
    print('\t\t\t\t+------------------------------------------------------+')

def register_collector_success_screen():
    clear_screen()
    print('\t\t\t\t+------------------------------------------------------+')
    print('\t\t\t\t|                                                      |')
    print('\t\t\t\t|        COLECIONADOR REGISTRADO COM SUCESSO           |')
    print('\t\t\t\t|                                                      |')
    print('\t\t\t\t+------------------------------------------------------+')
    sleep(5)

def close_application_screen():
    clear_screen()
    print('\t\t\t\t+------------------------------------------------------+')
    print('\t\t\t\t|                                                      |')
    print('\t\t\t\t|    A APLICACAO SERA FECHADA  CONFORME SOLICITADO     |')
    print('\t\t\t\t|                                                      |')
    print('\t\t\t\t+------------------------------------------------------+')
    sleep(5)
    clear_screen()
