from bs4 import BeautifulSoup as bs
import requests
import sqlite3
import os

def create_table() ->  None:
    con = sqlite3.connect('db.sqlite3')
    cursor = con.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS pictures (
                       name TEXT UNIQUE NOT NULL
                   )
                   """)
    con.commit()
    con.close()

def in_db(name_: str) -> bool:
    con = sqlite3.connect('db.sqlite3')
    cursor = con.cursor()
    cursor.execute(f"""
                   SELECT * FROM pictures WHERE name='{name_}'
                   """)
    row = cursor.fetchone()
    con.close()
    return row is not None
    
def add_to_db(name_):
    con = sqlite3.connect('db.sqlite3')
    cursor = con.cursor()
    cursor.execute(f"""
                   INSERT INTO pictures (name)
                   VALUES ('{name_}')
                   """)
    con.commit()
    con.close()


def download_pictures() -> None:
    with open('index.html') as f:
        
        soup = bs(f.read(), 'html.parser')
        for tag in soup.find_all('img'):
            src = tag.get('src')
            name = src[-15:-5] + '.jpg'
            if not in_db(name_=name):
                add_to_db(name_=name)
                response = requests.get(src)
                if response.status_code == 200:
                    picture = response.content
                with open('downloads/' + name, 'wb') as f:
                    f.write(picture)

if __name__ == '__main__':
    if not os.path.exists('donwnloads/'):
        os.mkdir('downloads/')
    create_table()
    download_pictures()