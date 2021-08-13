import sqlite3
import requests
from bs4 import BeautifulSoup


def StoreData(que, ans):
    conn = None
    try:
        print("Connecting....")
        conn = sqlite3.connect('xyz.db')
        print("Connected")
    except Error as e:
        print(e)

    sql = '''INSERT INTO MyData (Question, Answer)
                VALUES(?, ?)'''
    cur = conn.cursor()

    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='MyData' ''')
    # if the count is 1, then table exists
    if cur.fetchone()[0] == 1:
        {
            print('Table exists.')
        }
    else:
        cur.execute("CREATE TABLE MyData (Question TEXT, Answer TEXT)")
        print(":)...  Table is created")

    val = (que, ans)
    cur.execute(sql, val)
    print('Detail Inserted  😎 ')
    conn.commit()


def Scrap():
    res = requests.get('https://www.udemy.com/topic/python/')
    soup = BeautifulSoup(res.content, 'lxml')
    all_faq = soup.findAll('div', {'class': 'panel--panel--3uDOH'})

    for a in all_faq:
        faq_que = a.find('span', {'class': 'udlite-accordion-panel-title'})
        faq_ans = a.find('div', {'class': 'panel--content-wrapper--1g5eE'})
        print('Question : ' + faq_que.get_text())
        print('Answer : ' + faq_ans.get_text())
        StoreData(faq_que.get_text(), faq_ans.get_text())


Scrap()
