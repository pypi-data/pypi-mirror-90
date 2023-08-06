import os
import shutil

def ask(text):
    while (r:=input(text+' [Y/N]: ').lower()) not in ['y','n']:
        continue
    
    return r == 'y'

def mkpath(path):
    print(f'Making path "{path}"')
    try:
        if os.path.exists(path):
            if ask(f'"{path}" directory found. Overwrite?'):
                shutil.rmtree(path)
            else:
                return False
        os.makedirs(path, exist_ok=True)
        return True
    except OSError as e:
        print(f'Can`t make path "{path}": {str(e)}')
        return False

def mkfile(path, content):
    print(f'Making file "{path}"')
    if os.path.exists(path):
        if ask(f'"{path}" file found. Overwrite?'):
            os.remove(path)
        else:
            return False
    
    with open(path, 'w+', encoding='utf-8') as file:
        file.write(content)
        file.close()
