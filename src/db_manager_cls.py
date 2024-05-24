import psycopg2

red_col = '\033[91m'
reset_red_col = '\033[0m'

class DBManager():
    '''для организации подключения и вывода различной информации из БД по определенным критериям'''
    def __init__(self, con):
        self.con = con

    def get_companies_and_vacancies_count(self):
        '''получает список всех компаний и количество вакансий у каждой компании.'''
        try:
            with self.con:
                with self.con.cursor() as cur:
                    cur.execute('SELECT  employers.employer, COUNT(*) FROM vacancies '
                                'JOIN employers USING(employer_id)'
                                'GROUP BY employers.employer')
                    rows = cur.fetchall()
                    for i in rows:
                        print(f"компания - {''.join(i[0])}, количество вакансий - {i[1]}")

        except psycopg2.Error as e:
            print(f"произошла {e.pgerror}")
            print(f"код ошибки: {e.pgcode}")

    def get_all_vacancies(self):
        ''''получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.'''
        try:
            with self.con:
                with self.con.cursor() as cur:
                    cur.execute('SELECT * FROM vacancies')
                    rows = cur.fetchall()

                    for i in rows:
                        print(f'{i} \n {"-" * 200}')

        except psycopg2.Error as e:
            print(f"произошла {e.pgerror}")
            print(f"код ошибки: {e.pgcode}")

    def get_avg_salary(self, currency: str = "RUR"):
        '''получает среднюю зарплату по вакансиям. по умолчанию "RUR" '''
        try:
            with self.con:
                with self.con.cursor() as cur:
                    cur.execute(f"SELECT AVG(salary) "
                                f"FROM vacancies "
                                f"WHERE vacancies.currency = %s", (currency, ))
                    rows = cur.fetchall()
                    decimal_value = rows[0][0]
                    if decimal_value is not None:
                        print(f"{red_col}средняя зарплата - {int(decimal_value)} {currency}{reset_red_col}")

                    else: print(f"{red_col}валюта {currency} отсутствует в базе данных! {reset_red_col}")


        except psycopg2.Error as e:
            print(f"произошла {e.pgerror}")
            print(f"код ошибки: {e.pgcode}")

    def get_vacancies_with_higher_salary(self, currency: str = "RUR"):
        ''' получает список всех вакансий, у которых зарплата выше средней по всем вакансиям. по умолчанию "RUR"'''
        try:
            with self.con:
                with self.con.cursor() as cur:
                    cur.execute(f"SELECT * FROM vacancies WHERE currency = %s "
                                f"AND salary > (SELECT AVG(salary) "
                                f"FROM vacancies "
                                f"WHERE currency = %s)", (currency, currency))
                    rows = cur.fetchall()

                    for i in rows:
                        print(f'{i} \n {"-" * 200}')

        except psycopg2.Error as e:
            print(f"произошла {e.pgerror}")
            print(f"код ошибки: {e.pgcode}")

    def get_vacancies_with_keyword(self, keyword):
        '''получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.'''
        try:
            with self.con:
                with self.con.cursor() as cur:
                    like_pattern = f'%{keyword}%'
                    cur.execute(f"SELECT * FROM vacancies "
                                f"WHERE vacancy LIKE %s", (like_pattern,))
                    rows = cur.fetchall()
                    for i in rows:
                        print(f'{i} \n {"-" * 200}')

        except psycopg2.Error as e:
            print(f"произошла {e.pgerror}")
            print(f"код ошибки: {e.pgcode}")

    def get_all_currency(self):
        ''''получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.'''
        try:
            with self.con:
                with self.con.cursor() as cur:
                    cur.execute('SELECT DISTINCT currency FROM vacancies')
                    rows = cur.fetchall()

                    for i in rows:
                        print(f'{red_col}{", ".join(i)}{reset_red_col}')

        except psycopg2.Error as e:
            print(f"произошла {e.pgerror}")
            print(f"код ошибки: {e.pgcode}")

    def con_close(self):
        '''закрывает соединение с БД'''
        if self.con:
            self.con.close()
