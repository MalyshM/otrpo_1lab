from ftplib import FTP
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from datetime import date
import os
from fastapi import HTTPException
import threading

from schemas import Pokemon


async def save_pokemon_to_FTP(pokemon):
    ftp_address = 'ftp'
    ftp_username = 'myuser'
    ftp_password = 'change_this_password'
    ftp_base_directory = ''  # Updated base directory

    ftp = FTP()
    ftp.connect(ftp_address, 2121)
    ftp.login(ftp_username, ftp_password)

    markdown_template = '''\
    # {name}

    - height: {height}
    - hp: {hp}
    - attack: {attack}
    - defence: {defence}
    - speed: {speed}
    - picture: {picture}
    '''
    dict_ = pokemon.dict()
    if None in dict_.values():
        ftp.quit()
        raise HTTPException(status_code=400, detail='Invalid Pokémon information')
    else:
        markdown_content = markdown_template.format(
            name=dict_['name'],
            height=dict_['height'],
            hp=dict_['hp'],
            attack=dict_['attack'],
            defence=dict_['defence'],
            speed=dict_['speed'],
            picture=dict_['picture'],
        )
        today = date.today()
        folder_name = today.strftime('%Y%m%d')
        ftp_folder_path = os.path.join(ftp_base_directory, folder_name)
        try:
            ftp.mkd(ftp_folder_path)
        except:
            pass
        ftp.cwd(ftp_folder_path)

        file_name = f'{dict_["name"]}.md'
        file_path = os.path.join(file_name)  # Specify the full file path
        print(file_path)
        with open(file_path, 'w') as f:
            f.write(markdown_content)
            print(markdown_content)

        with open(file_path, 'rb') as f:
            ftp.storbinary(f'STOR {file_name}', f)
            print(f'STOR {file_name}')

        # ftp.quit()
        return {'message': 'Pokémon information saved successfully'}

# if __name__ == '__main__':
#     thread = threading.Thread(target=save_pokemon_to_FTP, args=(
#     Pokemon(name="asd", height=12, hp=32, attack=34, defence=54, speed=56, picture="asd"),))
#     thread.start()
#
# make_ftp_server()
