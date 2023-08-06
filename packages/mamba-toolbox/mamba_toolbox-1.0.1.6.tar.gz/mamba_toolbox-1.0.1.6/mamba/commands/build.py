from os import path
from os.path import relpath
import click
import shutil
import os
import json
import hashlib
from json import JSONDecodeError
from zipfile import ZipFile

def get_config():
    try:
        return json.loads(open(os.path.join(os.getcwd(), 'mamconf.json')).read())
    except FileNotFoundError as e:
        print('Fatal: Mamba build configuration not found: '+str(e))
    except JSONDecodeError as e:
        print('Fatal: Unnable to parse json config: '+str(e))
    
    exit()

def rc4_encrypt(data, key):
    x = 0
    box = list(range(256))
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = 0
    y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append((ord(char)  ^ box[(box[x] + box[y]) % 256]).to_bytes(2, byteorder='big'))
    return b''.join(out)
   

@click.command('build')
def build_package():
    config = get_config()
    PROJECT_NAME = config['project_name']
    SRC_PROJECT_FOLDER = os.path.join(os.getcwd(), PROJECT_NAME)
    KEY = hashlib.md5(config['crypt_key'].encode()).hexdigest().upper()
    # IGNORED = [os.path.abspath(x) for x in config['builder']['ignore']]
    TOCOPY = config['builder']['tocopy']
    BUILD_HERE = os.path.abspath(config['builder']['build_folder'])
    DST_PROJECT_FOLDER = os.path.join(BUILD_HERE, PROJECT_NAME)
    DIST_HERE = os.path.abspath(config['builder']['distribution_folder'])
    EXT = '.mb'
    
    print('Checking folders...')
    if not os.path.exists(SRC_PROJECT_FOLDER):
        print(f'Fatal: src project folder "{SRC_PROJECT_FOLDER}" not found.')
        exit()
    print('SRC project folder OK')

    os.makedirs(DST_PROJECT_FOLDER, exist_ok=True)
    print('DST project folder OK')
    os.makedirs(DIST_HERE, exist_ok=True)
    print('Distribution folder project folder OK')

    # copy "tocopy"

    for route in TOCOPY:
        os.makedirs(os.path.dirname(os.path.join(BUILD_HERE, route)), exist_ok=True)
        if os.path.isfile(route):
            print(f'Copying file {route}')
            shutil.copyfile(os.path.abspath(route), os.path.join(BUILD_HERE, route))
        else:
            print(f'Copying tree {route}')
            shutil.rmtree(os.path.join(BUILD_HERE, route))
            shutil.copytree(os.path.abspath(route), os.path.join(BUILD_HERE, route))

    for root, _, file_list in os.walk(SRC_PROJECT_FOLDER):
        for file_item in file_list:
            src = os.path.join(root, file_item)
            dst = os.path.join(BUILD_HERE, os.path.relpath(root), file_item)
            
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if (file_item.split('.')[-1] != "py"):
                print(f'Copying {src}')
                shutil.copyfile(src, dst)
            else:
                print(f'Encrypting {file_item}')
                with open(src, 'r', encoding='utf-8') as py:
                    with open(dst.replace('.py', EXT), 'wb+') as mb:
                        mb.write(rc4_encrypt(py.read(), KEY))
                        # mb.write(py.read().encode())

    print('Build finished!')

    



        