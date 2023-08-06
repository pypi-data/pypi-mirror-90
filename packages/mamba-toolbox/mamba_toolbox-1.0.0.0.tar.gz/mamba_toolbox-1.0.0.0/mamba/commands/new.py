from os.path import join
import click
import os
from ..tools import mkfile, mkpath, ask 
import json
from datetime import datetime
import hashlib

@click.command('new')
@click.argument('name')
@click.option('--folder', default='.', help='Path to new project. Current dir is default')
def new_project(name, folder):
    folder = os.path.abspath(folder)
    print(f'Making new project "{name}" in "{folder}"')
    if folder != os.getcwd():
        mkpath(folder)
    mkfile(os.path.join(folder, 'mamconf.json'), 
        json.dumps({
            "project_name": name,
            "crypt_key": hashlib.md5(datetime.now().isoformat().encode()).hexdigest(),
            "dependencies": [],
            "builder": {
                "ignore": [
                    "run.py", 
                    "mamconf.json",
                    ".gitignore",
                    "venv"],
                "copy_asis": [],
                "pythonversion": 38,
                "output": '../build'
            }
        }, indent=2))
    mkfile(os.path.join(folder, 'run.py'), 
        f"""from {name}.__main__ import start

if __name__ == "__main__":
    start()
""")
    mkpath(os.path.join(folder, name))
    mkfile(os.path.join(folder, name, '__main__.py'), 
            f"""# -*- encoding=utf-8 -*-
# This file was generated automatically

__version__ = (1,0,0,0)

def start():
    try:
        print("{name} v"+".".join(str(x) for x in __version__))
        # YOUR CODE HERE
        pass
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    start()
                """)

    if ask('Create virtual environment for this project?'):
        os.chdir(folder)
        os.system('virtualenv venv')

    if ask('Create ".gitignore" file?'):
        mkfile('.gitignore', """.vscode
venv
build
dist
*/__pycache__""")

    if ask('Initialize new git repository?'):
        os.system('git init')

            


