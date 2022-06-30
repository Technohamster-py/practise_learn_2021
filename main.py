"""
----------------------------------------------
Programm by: Technohamster

Python verion:          Year:
        3.9             2021

Thank you for using my programm! Good luck)
----------------------------------------------
"""

import requests
from bs4 import BeautifulSoup
from config import *
import pymysql
from datetime import datetime


def connect_to_db():

    try:
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            create_table_req = f"CREATE TABLE IF NOT EXISTS {tbl_name} (" \
                               "pull_date date," \
                               "currency varchar(3)," \
                               "course float);"
            cursor.execute(create_table_req)  # Создаем таблицу, если ее еще нет

        return connection

    except Exception as exeption:
        print(f"Can't connect to database: {exeption}")
        return False


def add_data(courses: dict, names: dict):
    """
    Добавление данных в таблицу
    :param courses: курсы валют сегодня
    :param names: соотношения кодов влют и их полных названий
    :return: None
    """
    connection = connect_to_db()
    date = datetime.today()
    if connection:
        with connection.cursor() as cursor:
            select_req = f"SELECT pull_date from {tbl_name} WHERE pull_date = {date};"
            cursor.execute(select_req)
            rows = cursor.fetchall()
            if not rows:
                for currency in names:
                    course = courses[currency]

                    add_req = f"INSERT INTO {tbl_name} (pull_date, currency, cource)" \
                              f"VALUES ({date}, {currency}, {course});"
                    cursor.execute(add_req)
                    connection.commit()
        connection.close()


def get_updates():
    """
    Получение курсов валют с сайта ЦБ РФ
    :return: словарь с курсами единицы валюты по отношению к рублю,
    словарь с наименованиями валют и их буквенными кодами.
    """
    courses = {'Российский рубль': 1}
    names = {'RUB': 'Российский рубль'}
    try:
        soup = BeautifulSoup(requests.get(URL).text, features="html.parser")  # Получение исходного кода страницы
        table = soup.find('table', {'class': 'data'})  # Нахождение таблицы на странице
        for currency in table.findAll('tr'):  # Проходим таблицу построчно
            line = []
            if 'код' not in currency.text:  # Отсекаем строку заголовков
                for cell in currency.text.split('\n'):  # Получаем значения ячеек
                    if cell:
                        line.append(cell)  # Формируем список для удобства обращения к значениям из строки
                names[line[1]] = line[3]
                course = float(line[4].replace(',', '.')) / float(line[2])  # Высчитываем курс за одну единицу валюты
                courses[line[3]] = course
    except:
        print(CONNECTION_ERROR_MESSAGE)
        quit()
    return courses, names


def help(names: dict):
    """
    Вывод списка кодов и имен доступных валют
    :param names: словарь с кодами и именами
    :return: None
    """
    for code in names.keys():
        print(names[code], '\t', code)


def convert(courses: dict, source_currency, required_currency, summ=1):
    """
    Конвертация валют. В случае перевода не из рублей производится сначала перевод в рубли, а потом из рублей в
    необходимую валюту.
    :param courses: словарь с курсами валют
    :param source_currency: код исходной валюты
    :param required_currency: код необходимой валюты
    :param summ: сумма в исходной валюте
    :return:
    """
    if source_currency == 'RUB':
        new_summ = summ / courses[required_currency]
        new_summ = round(new_summ, 2)
    else:
        new_summ = summ * courses[source_currency] / courses[required_currency]
        new_summ = round(new_summ, 2)

    return new_summ


if __name__ == '__main__':
    courses, names = get_updates()

    while True:
        command = input(MENU_MESSAGE)
        if command.lower() == 'help':
            help(names)
        elif command.lower() == 'stop':
            quit()
        elif command.lower() == 'update':
            courses, names = get_updates()
        else:
                try:
                    source = command.split()[0].upper()
                    if source in names.keys():
                        source = names[source]
                        summ = int(command.split()[1])
                        required = input('Введите код валюты, в которую хотите перевести\n').upper()
                        required = names[required]
                        if required in courses.keys():
                            print(f'{summ} {source} = {convert(courses, source, required, summ)} {required}')
                        else:
                            print(ERROR_MESSAGE)
                except:
                    print(ERROR_MESSAGE)
