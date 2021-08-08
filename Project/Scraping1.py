import time
import sqlite3
import pandas as pd # pip install pandas
# pip install selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup # pip install beautifulsoup4

conn = None
try:
    print("Connecting....")
    conn = sqlite3.connect('xyz.db')
    print("Connected")
except Error as e:
    print(e)

sql = '''INSERT INTO MyData (course_title, author, course_rating, course_price)
            VALUES(?, ?, ?, ?)'''
cur = conn.cursor()

cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='MyData' ''')
#if the count is 1, then table exists
if cur.fetchone()[0]==1 : {
	print('Table exists.')
}
else:
    cur.execute("CREATE TABLE MyData (course_title TEXT, author TEXT, course_rating FLOAT, course_price FLOAT)")
    print(":)...  Table is created")


sort_by_type = 'newest'

chrome_driver_path = 'chromedriver.exe'
delay = 15

driver = webdriver.Chrome(chrome_driver_path)

def extract_text(soup_obj, tag, attribute_name, attribute_value):
    txt = soup_obj.find(tag, {attribute_name: attribute_value}).text.strip() if soup_obj.find(tag, {attribute_name: attribute_value}) else ''
    return txt

rows = []

for page_number in range(1, 4):
    page_url = f'https://www.udemy.com/topic/python/'
    driver.get(page_url)
    time.sleep(5)

    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'course-list--container--3zXPS')))
    except TimeoutException:
        print('Loading exceeds delay time')
        break
    else:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        course_list = soup.find('div', {'class': 'course-list--container--3zXPS'})
        courses = course_list.find_all('a', {'class': 'udlite-custom-focus-visible browse-course-card--link--3KIkQ'})

        for course in courses:
            course_title = course.select('div[class*="course-card--course-title"]')[0].text
            author = extract_text(course, 'div', 'data-purpose', 'safely-set-inner-html:course-card:visible-instructors')
            course_rating = extract_text(course, 'span', 'data-purpose', 'rating-number')
            course_price = extract_text(course, 'div', 'data-purpose', 'course-price-text')

            val = (course_title, author, course_rating, course_price)
            cur.execute(sql,val)
            print('Detail Inserted  😎 ')

conn.commit()
print("Ok")

