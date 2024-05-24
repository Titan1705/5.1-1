import time

from src.api_hh_cls import HHApi
from src.api_hh_cls import VacanciesParser
from src.db_manager_cls import DBManager
from src.utils import connector
from src.utils import tables_creator
from src.utils import loads_into_table
from src.utils import drop_table

red_col = '\033[91m'
reset_red_col = '\033[0m'


def main():
    '''пользовательский интерфейс приложения'''
    con = connector('database.ini')
    drop_table(con, 'vacancies', 1)
    drop_table(con, 'employers',1)

    hh_api_instance = HHApi()

    page_quantity = input('Введите количество запрашиваемых страниц от 1 до 20: ')
    if page_quantity.isdigit() and 0 < int(page_quantity) <=20:
        hh_api_instance.load_vacancies(page_quantity, int(page_quantity)) #запрос через апи
    else:
        print(f'{red_col}вы ввели неверный параметр, по умолчанию будет загружено 2 страницы{reset_red_col}')
        time.sleep(1)
        hh_api_instance.load_vacancies() #запрос через апи

    vacancies_list = hh_api_instance.vacancies
    parser_inst = VacanciesParser()
    vacancies_inst_list = parser_inst.parser_api_vacancies(vacancies_list)
    tables_creator(con, 1)
    loads_into_table(con, vacancies_inst_list,1)
    db_man_inst = DBManager(con)

    while True:

        print('''1 - вывести на экран список всех компаний и количество вакансий у каждой компании
2 - вывести на экран список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
3 - вывести на экран среднюю зарплату по вакансиям. (по умолчанию RUR)
4 - вывести на экран список всех вакансий, у которых зарплата выше средней по всем вакансиям. (по умолчанию "RUR")
5 - вывести на экран список всех валют среди загруженных вакансий
6 - вывести на экран список всех вакансий, в названии которых содержится ключевое слово.
0 - завершение программы
''')
        choice_number = ['1', '2', '3', '4', '5', '6', '0']
        user_choice = input(f"{'⛔' * 110}\nВведите номер и нажмите 'enter' для пуска действия: ")

        if user_choice and user_choice == '1' and user_choice in choice_number:
            db_man_inst.get_companies_and_vacancies_count()

        elif user_choice and user_choice == '2' and user_choice in choice_number:
            db_man_inst.get_all_vacancies()

        elif user_choice and user_choice == '3' and user_choice in choice_number:
            user_input = input('введите валюту: ')
            if user_input.isalpha():
                db_man_inst.get_avg_salary(user_input.upper())
            else: print(f"{red_col}посмотрите список валют (команда №5) и попробуйте еще раз) {reset_red_col}")

        elif user_choice and user_choice == '4' and user_choice in choice_number:
            user_input = input('введите валюту: ')
            if user_input.isalpha():
                db_man_inst.get_vacancies_with_higher_salary(user_input.upper())
            else:
                print(f"{red_col}посмотрите список валют (команда №5) и попробуйте еще раз) {reset_red_col}")

        elif user_choice and user_choice == '5' and user_choice in choice_number:
            db_man_inst.get_all_currency()

        elif user_choice and user_choice == '6' and user_choice in choice_number:
            user_input = input('введите ключевое слово: ')
            db_man_inst.get_vacancies_with_keyword(user_input)

        elif user_choice and user_choice == '0' and user_choice in choice_number:
            db_man_inst.con_close()
            break


if __name__ == '__main__':
    main()
