import sqlite3
import hashlib
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 8501))

server.listen()

def handle_connection(c):
    hwid = c.recv(1024).decode()
    key = c.recv(1024)
    key = hashlib.sha256(key).hexdigest()

    con = sqlite3.connect("userdata.db")
    cur = con.cursor()

    cur.execute("SELECT * FROM userdata WHERE hwid = ? AND key = ?", (hwid, key))

    if cur.fetchall():
        c.send(b"yes")
        print("yes")
    else:
        c.send(b"no")
        print("no")

while True:
    client, addr = server.accept()
    threading.Thread(target=handle_connection, args=(client,)).start()