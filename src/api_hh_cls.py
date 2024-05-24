import requests
from abc import ABC, abstractmethod


class Vacancy():
    '''Класс для организации данных по вакансиям в удобном виде. хранит в себе полезные атрибуты по вакансиям'''

    def __init__(self, region, employer_id, employer_name, vacancy_name, salary, currency, requirement, vacancy_url):
        self.region = region
        self.employer_id = employer_id
        self.employer_name = employer_name
        self.vacancy_name = vacancy_name
        self.salary = salary
        self.currency = currency
        self.requirement = requirement
        self.vacancy_url = vacancy_url

    def __str__(self):
        cut_line = '-' * 120
        return f'''{cut_line}

area: {self.region}, employer_id: {self.employer_id}, employer_name: {self.employer_name}, vacancy: {self.vacancy_name}, salary: {self.salary} {self.currency}, 
requirement: {self.requirement})
vacancy_url: {self.vacancy_url}
'''

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __lt__(self, other):
        if self.salary is not None and other.salary is not None:
            return self.salary < other.salary


class Parser(ABC):
    @abstractmethod
    def load_vacancies(self):
        pass


# employers_id = [10413982, 46926]

employers_ids = {
    108780: 'СКАУТ Разработчик Системы',
    3432635: 'ООО EVOS',
    9196211: 'JFoRecruitment',
    6000512: 'ООО Долсо',
    656481: 'Biglion',
    1577237: 'ООО Эрвез',
    5879545: 'ООО Фаст Софт',
    10882430: 'Лаборатория айти',
    2437802: 'ООО Леон',
    1740: 'яндекс'
}


class HHApi(Parser):
    """
    Класс для работы с API HeadHunter
    Класс Parser является родительским классом, который вам необходимо реализовать
    """
    employers_data = employers_ids

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'employer_id': '', 'page': 0, 'per_page': 100, 'only_with_salary': 'true'}
        self.vacancies = []

    def load_vacancies(self, keyword: str = '', page_quantity: int = 2):  # page_quantity задаем от 0  до 20
        '''загружает данные c АПИ'''
        self.params['text'] = keyword
        self.params['employer_id'] = self.employers_data
        while self.params.get('page') != page_quantity:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1


class VacanciesParser():
    """
    Класс для парсинга данных с АПИ
    """

    def parser_api_vacancies(self, api_data: list):
        '''парсит данные c апи по определенным критериям'''
        vacancies_list = []

        for data in api_data:
            vacancy_name = data.get('name')
            salary = data.get('salary')
            if salary and salary.get('from'):
                filtered_salary = salary['from']
            else:
                filtered_salary = 0
            snippet = data.get('snippet')
            if salary:
                salary = data.get('salary')
                currency = salary.get('currency')
            else:
                currency = ''
            requirement = snippet.get('requirement')
            if requirement:
                requirement = requirement.replace('<highlighttext>', '').replace('</highlighttext>', '')
            else:
                requirement = 'нет требований'
            vacancy_url = data.get('alternate_url')
            area = data.get('area')
            region = area.get('name')

            employer = data.get('employer')
            employer_id = employer.get('id')
            employer_name = employer.get('name')

            vacancy_instance = Vacancy(region, employer_id, employer_name, vacancy_name, filtered_salary, currency,
                                       requirement, vacancy_url)

            vacancies_list.append(vacancy_instance)
        return vacancies_list
