import getpass
import fake_useragent
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

def calculate():
    driver.get(resp)
    wait = WebDriverWait(driver, 10)
    wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'mtable')))
    elem_marks = driver.find_elements(By.XPATH, ".//td[contains(concat(' ', @class, ' '), ' lesson_exists ') or contains(concat(' ', @class, ' '), ' lesson_exists-')]//span")
    all_marks = [mark.text for mark in elem_marks]
    driver.quit()
    return all_marks


s = requests.Session()
user = fake_useragent.UserAgent().random

url = 'https://schools.by/login'
s.get(url)
token = s.cookies['csrftoken']


data = {
    'csrfmiddlewaretoken': token,
    'username' : 'empty',
    'password' : 'empty',
    '|123': '|123'
}

header = {
    'user-agent': user,
    'referer': url
}

data['username'] = input('Введите логин: ')
data['password'] = getpass.getpass('Введите пароль: ')

logs = s.post(url, data=data, headers=header)
resp = logs.url + '#progress'
settings = Options()
settings.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=settings)
driver.get(resp)

if resp == 'https://schools.by/login#progress':
    driver.quit()
    print('Данные введены неверно. Не удалось войти.')
    input()
    exit(1)

for cookie in s.cookies:
    driver.add_cookie({'name': cookie.name, 'value': cookie.value})

raw_marks = calculate()
marks = []
for mark in raw_marks:
    if '/' in mark:
        marks.extend(mark.split('/'))
    else:
        marks.append(mark)

marks = [x for x in marks if x.isdigit()]
marks = list(map(int, marks))
total = sum(marks) / len(marks)
print(f'Успешно вычислено! Ваш средний балл по всем оценкам: {round(total, 2)}')
