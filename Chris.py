import sys
import os
import re
import ChrisFileManager


def new_project(name='', target_path=''):
    os.chdir('database')
    save_file = re.compile(name + r'-(\d)+' + '.chris')
    target = os.path.join(target_path, name)
    if not os.path.exists(target):
        os.mkdir(target)
    DNE = True
    for entry in os.listdir(os.getcwd()):
        if save_file.search(entry) is not None:
            print('PROJECT OF THIS NAME ALREADY EXISTS')
            DNE = False
            break
    if DNE:
        ChrisFileManager.ChrisWriter(name, target).write_chris_file()


def get_projects():
    os.chdir('database')
    projects = []
    for entry in os.listdir(os.getcwd()):
        if entry.find('.chris') > 0:
            name = entry[0:entry.rindex('-')]
            if name not in projects:
                projects.append(name)
    return projects


def show_projects():
    projects = get_projects()
    for project in projects:
        print(project)


def get_saves(name=""):
    os.chdir('database')
    saves = []
    for entry in os.listdir(os.getcwd()):
        if entry.find('.chris') > 0 and entry.find(name) > -1:
            saves.append(entry[0:entry.index('.chris')])
    return saves


def show_saves(name=""):
    saves = get_saves(name)
    saves.sort()
    saves.reverse()
    for save in saves:
        print(save)


def get_recent_save(name=""):
    num = -1
    for save in get_saves(name):
        save_num = int(save[save.rindex('-') + 1:])
        if save_num > num:
            num = save_num
    return num


def new_save(name="", project_path=""):
    num = get_recent_save(name)
    previous = num
    if num == -1:
        previous = 'None'
    ChrisFileManager.ChrisWriter(name, project_path).write_chris_file(num + 1, previous)


def load_save(save="", target_path=""):
    os.chdir('database')
    save_file = save + '.chris'
    if save_file in os.listdir(os.getcwd()):
        target = os.path.join(os.getcwd(), save_file)
        ChrisFileManager.ChrisReader(target).recreate_project(target_path)
    else:
        print('INVALID SAVE')


def quick_save(name="", project_path=""):
    num = get_recent_save(name)
    if num == -1:
        new_save(name, project_path)
    else:
        save_file = name + '-' + str(num) + '.chris'
        os.remove(save_file)
        new_save(name, project_path)


def commands():
    if len(sys.argv) == 2:
        if sys.argv[1] == 'show_projects':
            show_projects()
        else:
            print('ARGUMENTS ERROR')
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'show_saves':
            show_saves(sys.argv[2])
        else:
            print('ARGUMENTS ERROR')
    elif len(sys.argv) == 4:
        if sys.argv[1] == 'new_project':
            new_project(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'new_save':
            new_save(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'load_save':
            load_save(sys.argv[2], sys.argv[3])
        else:
            print('ARGUMENTS ERROR')
    else:
        print('INVALID ARGUMENTS')


if __name__ == '__main__':
    commands()
