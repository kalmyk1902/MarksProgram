"""

КОММЕНТАРИИ К ПРОГРАММЕ ВЫЧИСЛЕНИЯ СРЕДНЕГО БАЛЛА
Эта программа вычисляет средний балл на основании
выставленных отметок на платформе schools.by

"""

#импортируем нужные библиотеки
import getpass
import fake_useragent
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

#функция поиска отметок
def calculate():
    driver.get(resp) #входим на сайт
    wait = WebDriverWait(driver, 10) #задаем параметры ожидания в 10 секунд
    wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'mtable'))) #ожидаем загрузки таблицы успеваемости
    elem_marks = driver.find_elements(By.XPATH, ".//td[contains(concat(' ', @class, ' '), ' lesson_exists ') or contains(concat(' ', @class, ' '), ' lesson_exists-')]//span") #при помощи XPath-выражения извлекаем данные об отметках и пропусках
    all_marks = [mark.text for mark in elem_marks] #записываем все в массив
    driver.quit() #выходим с сайта
    return all_marks #функция возвращает список


s = requests.Session() #запускаем сессию
user = fake_useragent.UserAgent().random #представляемся системе как рандомный браузер

url = 'https://schools.by/login' #объявляем переменную с ссылкой входа
s.get(url) #заходим в нее
token = s.cookies['csrftoken'] #получаем токен сессии (без него сайт нас не пустит)

#данные для отправки на сервер (при входе на сайт)
data = {
    'csrfmiddlewaretoken': token, #токен сессии
    'username' : 'empty', #логин
    'password' : 'empty', #пароль
    '|123': '|123' #без этого сервер не примет запрос
}

#метаданные запроса
header = {
    'user-agent': user, #откуда отправили запрос (в нашем случае с любого браузера)
    'referer': url #кто отправил запрос (в нашем случае сайт для входа)
}

data['username'] = input('Введите логин: ') #просим ввести логин
data['password'] = getpass.getpass('Введите пароль: ') #просим ввести пароль

logs = s.post(url, data=data, headers=header) #отправляем данные на сервер
resp = logs.url + '#progress' #получаем ссылку в качестве ответа
settings = Options() #задаем настройки
settings.add_argument('--headless') #отключаем интерфейс браузера
driver = webdriver.Chrome(chrome_options=settings) #входим в браузер
driver.get(resp) #заходим на полученную ссылку

if resp == 'https://schools.by/login#progress': #если мы остались на той же странице...
    driver.quit() #выходим с браузера
    print('Данные введены неверно. Не удалось войти.') #говорим об этом пользователю
    input() #ждем нажатия кнопки enter
    exit(0) #выходим с программы

for cookie in s.cookies: #собираем все cookie файлы для входа на сайт
    driver.add_cookie({'name': cookie.name, 'value': cookie.value}) #и передаем их браузеру

raw_marks = calculate() #используем ранее объявленную функцию для извлечения данных
marks = [] #создаем пустой список
for mark in raw_marks: #фильтруем список
    if '/' in mark: #если находим двойную отметку...
        marks.extend(mark.split('/')) #вписываем две отметки раздельно друг от друга
    else:
        marks.append(mark) #иначе просто записываем ее

marks = [x for x in marks if x.isdigit()] #отсеиваем все пропуски и пустые отметки
marks = list(map(int, marks)) #переводим в числовой тип данных
total = sum(marks) / len(marks) #вычисляем средний балл (сумму всех отметок делим на их количество)
print(f'Успешно вычислено! Ваш средний балл по всем оценкам: {round(total, 2)}') #выдаем результат пользователю с ограничением в 2 символа после точки