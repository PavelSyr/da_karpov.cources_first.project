import json
import sys

class Profile:
    def __init__(self, raw : dict, config_dir : str) -> None:
        self.path = f'{config_dir}/{raw["path"]}'

class Config:
    def __init__(self, raw : dict, config_dir : str) -> None:
        self.local = Profile(raw=raw['profiles']['local'], config_dir=config_dir)
        self.remote = Profile(raw=raw['profiles']['remote'], config_dir=config_dir)
        self.current = self.local

    def select_profile(self, name : str):
        if name == 'local':
            self.current = self.local
        elif name == 'remote':
            self.current = self.remote

class DataConfig:
    def __init__(self, raw : dict) -> None:
        self.name = raw['name']
        self.src = raw['src']

class DataCollection:
    def __init__(self, raw : dict) -> None:
        self.data = {}

        for i in raw['sources']:
            self.data[i] = DataConfig(raw['sources'][i])

def read_json(p : str) -> str:
    """ Try to read file and parse json
    
    p is string varible
    """
    try:
        with open(p) as json_file:
            f_json = json.load(json_file)
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror} for {p}")
    except: #handle other exceptions such as attribute errors
        print("Unexpected error:", sys.exc_info()[0])
    
    return f_json


def test_DataCollection(dc : DataCollection, names : list, config_path : str):
    good = True
    msg = 'тексты пройдены'

    if len(dc.data) != len(names):
        good = False
        msg = f'количество источников НЕ равно трём, нужно проверить содержимое файла {config_path}'

    # проверим что ожидаемые имена источников заданы
    for n in names:
        if n not in dc.data:
            good = False
            msg = f'{n} не найден в файле {config_path}'
            break

    # проверим что для всех источников указаны ссылки
    for n in names:
        d = dc.data[n]
        if d.src == '':
            good = False
            msg = f'поле src пустое в файле {config_path} для источника {n}\n{d.name}'
            break

    return (good, msg)