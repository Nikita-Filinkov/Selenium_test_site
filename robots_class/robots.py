import os
import time
import re

from pprint import pprint
from dadata import Dadata
from decouple import config

import requests
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


link = 'https://saby.ru/?redir=1'

options = webdriver.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/128.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")
# options.add_argument('headless')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(link)
contacts_batten = driver.find_element(By.CSS_SELECTOR, 'div[class="sbisru-Header-ContactsMenu js-ContactsMenu"]')
print(contacts_batten)
contacts_batten.click()
time.sleep(2)

contact_link = driver.find_element(By.CSS_SELECTOR, 'a[class="sbisru-link sbis_ru-link"]')
contact_link.click()
time.sleep(2)
print(contact_link)

tensor_link = driver.find_element(By.CSS_SELECTOR, 'a[title="tensor.ru"]')
tensor_link.click()
start_link = tensor_link.get_attribute('href')
time.sleep(2)
driver.quit()


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(start_link)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

element = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'div[class="tensor_ru-Index__block4-content tensor_ru-Index__card"]'))
)

block = element.find_element(By.CSS_SELECTOR, 'p[class="tensor_ru-Index__card-title tensor_ru-pb-16"]')
name_block = block.text
print(name_block)

paragraph = element.find_element(By.CSS_SELECTOR, 'p[class="tensor_ru-Index__card-text"]')
paragraph_link = paragraph.find_element(By.XPATH, './/a').get_attribute('href')

print(paragraph_link)
print(requests.get(paragraph_link).status_code)

driver.quit()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(paragraph_link)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

element = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'div[class="tensor_ru-container tensor_ru-section tensor_ru-About__block3"]'))
)

images = element.find_elements(By.CSS_SELECTOR, 'img')

width = set()
height = set()

for i in images:
    w = i.get_attribute('width')
    width.add(w)
    h = i.get_attribute('height')
    height.add(h)


print(len(width))
print(len(height))


def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        ip_info = response.json()
        return ip_info.get('ip')
    except requests.RequestException as e:
        print(f"Ошибка при получении внешнего IP: {e}")
        return None


id = get_public_ip()
if id:
    dadata = Dadata(config('TOKEN'))
    result = dadata.iplocate(id)
    pprint(result)
    region_with_type = result['data']['region_with_type']
    my_region = region_with_type.split()[0]
    pprint(region_with_type)
    pprint(my_region)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(link)
contacts_batten = driver.find_element(By.CSS_SELECTOR, 'div[class="sbisru-Header-ContactsMenu js-ContactsMenu"]')
contacts_batten.click()
time.sleep(2)
contact_link = driver.find_element(By.CSS_SELECTOR, 'a[class="sbisru-link sbis_ru-link"]')
contact_link.click()
time.sleep(2)
block_region = driver.find_element(By.CSS_SELECTOR, 'span[class="sbis_ru-Region-Chooser ml-16 ml-xm-0"]')
region = block_region.text.split()[0]
print(region)

partners = driver.find_elements(By.CSS_SELECTOR, 'div[data-qa="item"]')
old_city = partners[0].text
print(len(partners))
print(len(partners) > 0)
time.sleep(2)
block_region.click()
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, 'ul[class="sbis_ru-Region-Panel__list-l"]')
new_region = driver.find_element(By.CSS_SELECTOR, 'span[title="Камчатский край"]')
choice_region = new_region.text
new_region.click()
time.sleep(2)
block_region = driver.find_element(By.CSS_SELECTOR, 'span[class="sbis_ru-Region-Chooser ml-16 ml-xm-0"]')
region = block_region.text
print(region)
pattern_region = r'[^\d+\s]\w+\s\w+'
match_region = re.findall(pattern_region, choice_region)
print(region == match_region[0])

title = driver.title
print(title)
print(match_region[0])


match_title = re.findall(pattern_region, title)
print(match_title[1])
print(match_title[1] == match_region[0])

current_url = driver.current_url
print(current_url)
num_pattern_region = r'^\d+'
num_region_choice = re.findall(num_pattern_region, choice_region)
print(num_region_choice[0])

num_pattern_url = r'/(\d+)-'
num_region_url = re.findall(num_pattern_url, current_url)
print(num_region_url[0])
print(num_region_url[0] == num_region_choice[0])

new_partners = driver.find_elements(By.CSS_SELECTOR, 'div[data-qa="item"]')
new_city = new_partners[0].text
print(new_city)
print(old_city)

print(new_city != old_city)

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# link = 'https://saby.ru/'

driver.get(link)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(link)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

element = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'div[class="pt-56 pt-md-32 pt-sm-16"]'))
)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

try:
    download_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//a[contains(text(), 'Скачать локальные версии')]"))
    )
    link = download_link.get_attribute('href')  # Получаем значение атрибута href
    print("Ссылка на 'Скачать локальные версии':", link)
    download_link.click()
except Exception as e:
    print("Элемент не найден")

saby_pluging = driver.find_element(By.XPATH, "//div[@class='controls-TabButton__wrapper']//div[text()='Saby Retail']")
print(saby_pluging.is_enabled())
if not saby_pluging.is_enabled():
    saby_pluging.click()
windows = driver.find_element(By.XPATH, "//div[@class='controls-TabButton__caption']//span[text()='Windows']")
print(windows.is_enabled())
if not windows.is_enabled():
    windows.click()
download_file = driver.find_element(By.XPATH, "//a[contains(text(), 'Скачать (Exe 10.43 МБ)')]")

download_link_text = download_file.text
pattern_size = r'\s(\d+.\d+)\s'
size_on_site = re.findall(pattern_size, download_link_text)[0]
print(size_on_site)

print(download_link_text)
download_file_link = download_file.get_attribute('href')
print(download_file_link)

driver.quit()

try:
    response = requests.get(download_file_link)
    response.raise_for_status()
    pattern_name = r'win32/(.+\.exe)'
    file_name = re.findall(pattern_name, download_file_link)[0]

    with open(f'{file_name}', 'wb') as file:
        file.write(response.content)
    file_name = 'sbisplugin-setup-web.exe'
    file_size = os.path.getsize(f'{file_name}') / 1048576

    print(size_on_site in str(file_size))

except Exception as e:
    print("Ссылка не работает")