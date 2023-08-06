import os
import time
import shutil

def sort_photo():
    c_path = os.getcwd()
    file_list = os.listdir(c_path)
    result = {}

    for file_name in file_list:
        etime = os.path.getmtime(file_name)
        created = f"{c_path}/{time.strftime('%Y%m%d', time.localtime(etime))}"

        if created in result.keys():
            result[created].append(file_name)
        else:
            result[created] = []
            result[created].append(file_name)

    return result
    

def make_dir_move_file(path_dict):
    for path, file_list in path_dict.items():
        try:
            if not os.path.exists(path):
                os.makedirs(path)
                _move_file(file_list, path)
        except OSError:
            _move_file(file_list, path)

def _move_file(file_list, path):
    for file_name in file_list:
        shutil.move(file_name, f'{path}/{file_name}')

if __name__ == '__main__':
    path_dict = sort_photo()
    make_dir_move_file(path_dict)