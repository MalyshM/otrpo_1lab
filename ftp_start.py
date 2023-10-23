from ftplib import FTP
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from datetime import date
import os
from fastapi import HTTPException
import threading

from schemas import Pokemon


def make_ftp_server():
    # сюда нужно нереальное количество принтов для отладки
    FTP_PORT = 2121

    FTP_USER = "myuser"
    FTP_PASSWORD = "change_this_password"
    FTP_DIRECTORY = "/app/FTP"
    authorizer = DummyAuthorizer()
    authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='elradfmw')

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "pyftpdlib based ftpd ready."

    address = ('', FTP_PORT)
    server = FTPServer(address, handler)

    server.max_cons = 256
    server.max_cons_per_ip = 5

    server.serve_forever()



# if __name__ == '__main__':
#     thread = threading.Thread(target=save_pokemon_to_FTP, args=(
#     Pokemon(name="asd", height=12, hp=32, attack=34, defence=54, speed=56, picture="asd"),))
#     thread.start()
#
make_ftp_server()
