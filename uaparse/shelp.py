
import tkinter as tk
from tkinter import filedialog
import os
import json

current_path = os.path.dirname(os.path.realpath(__file__))

def browse_file_path(title_text="Choose File"):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes =(("json files", "*.json"),("All Files","*.*")),
                           title = title_text)
    return file_path


def copy_file_to(copyto,replace_file = False,title_text = 'Choose File'):

    already_exist = os.path.exists(copyto)
    if already_exist and not replace_file:
        print("File already exists")
    else:
        c_driver = browse_file_path(title_text=title_text)
        cdriver = None
        with open(c_driver,'rb') as f:
            cdriver = f.read()
        with open(copyto,'wb') as f:
            f.write(cdriver)
        print(f'copied {c_driver} to {copyto}')

copy_file_to(os.path.join(current_path ,'dbdata.json'))

def pgconnstring():
    connstring = None
    dbdata_file = os.path.join(current_path,'dbdata.json')
    with open(dbdata_file,'r',encoding='utf-8') as f:
        jobj = json.load(f)[0]
        user = jobj['user']
        password = jobj['password']
        host = jobj['host']
        dbname = jobj['dbname']
        connstring = f'postgresql+psycopg2://{user}:{password}@{host}/{dbname}'
    return connstring


