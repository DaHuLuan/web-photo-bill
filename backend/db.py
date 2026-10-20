import sqlite3
import time

DB_FILE = "bill.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        remark TEXT,
        img_path TEXT,
        create_time TEXT
    )
    ''')
    conn.commit()
    conn.close()

def add_bill(name, price, remark, img_path):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    t = time.strftime("%Y-%m-%d %H:%M:%S")
    cur.execute(
        "INSERT INTO bills(name,price,remark,img_path,create_time) VALUES (?,?,?,?,?)",
        (name, price, remark, img_path, t)
    )
    conn.commit()
    conn.close()

def get_bills():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM bills ORDER BY id DESC")
    data = res.fetchall()
    conn.close()
    ret = []
    for row in data:
        ret.append({
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "remark": row[3],
            "img_path": row[4],
            "create_time": row[5]
        })
    return ret

if __name__ == "__main__":
    init_db()
