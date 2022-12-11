from http.server import HTTPServer, CGIHTTPRequestHandler
import ssl
import time, datetime
import sqlite3
from threading import Thread

def Server():
    httpd = HTTPServer(('localhost', 5000), CGIHTTPRequestHandler)

    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ctx.load_cert_chain('ssl/server.crt', keyfile='ssl/server.key')
    httpd.socket = ctx.wrap_socket(httpd.socket)

    httpd.serve_forever()

def Timer():
    db = sqlite3.connect("Users.db")
    def Delete_db(fromm, value):
        db = sqlite3.connect("Users.db")
        db.row_factory = lambda cursor, row: row[0]
        db_req = f"DELETE FROM {fromm} WHERE time < '{value}';"
        db_value = db.cursor().execute(db_req)
        db.commit()

    while True: #бесконечный цикл с задержкой в один день, для удаления учетных записей и сообщений
        time.sleep(86400)
        time_now = datetime.datetime.now()
        Delete_db('users', time_now)
        Delete_db('secrets', time_now)

Thread(target=Timer).start()
Thread(target=Server).start()
