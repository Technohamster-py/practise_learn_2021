"""
----------------------------------------------
Programm by: Technohamster

Python verion:          Year:
        3.9             2021

Thank you for using my programm! Good luck)
----------------------------------------------
"""

URL = 'http://www.cbr.ru/currency_base/daily/'  # Адрес сайта-источника
MENU_MESSAGE = 'Введите код исходной валюты и сумму, которую хотите перевести \n' \
               'Например RUB 100 \n' \
               'Введите help, чтобы посмотреть коды валют\n' \
               'Введите update, чтобы обновить базу валют\n' \
               'Введите stop для выхода\n'
ERROR_MESSAGE = 'Проверьте правильность команды!'
CONNECTION_ERROR_MESSAGE = 'Невозможно получить данные, проверьте URL, подключение и перезапустите програму'

db_host = 'localhost'
db_user = 'root'
db_password = 'Thamster_SQL'
db_name = 'converter_db'
tbl_name = 'courses'
