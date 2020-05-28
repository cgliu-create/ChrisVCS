import sys
import os
import re
import ChrisFileManager


# Given a project a name and a location to create the project
# Accesses the database folder
# Checks than there are no chris files with this project name
# Creates a folder with the name of the project if it does not exist
# Creates a save 0 chris file
def createNewProjectAtPath(name='', target_path=''):
    os.chdir('database')
    save_file_pattern = re.compile(name + r'-(\d)+' + '.chris')
    target = os.path.join(target_path, name)
    if not os.path.exists(target):
        os.mkdir(target)
    DNE = True
    for entry in os.listdir(os.getcwd()):
        if save_file_pattern.search(entry) is not None:
            print('PROJECT OF THIS NAME ALREADY EXISTS')
            DNE = False
            break
    if DNE:
        ChrisFileManager.ChrisWriter(name, target).write_chris_file()


# Accesses the database folder
# Finds chris files
# Returns the unique project names from those files
def listNamesOfExistingProjects():
    os.chdir('database')
    projects = []
    for entry in os.listdir(os.getcwd()):
        if entry.find('.chris') > 0:
            name = entry[0:entry.rindex('-')]
            if name not in projects:
                projects.append(name)
    return projects


# Prints the result of get_projects
def displayNamesOfExistingProjects():
    projects = listNamesOfExistingProjects()
    for project in projects:
        print(project)


# Given the name of the project
# If the database folder is not already accessed, accesses the database folder
# Finds the chris files with this project name
# Returns the names of those chris files
def listNamesOfSavesForProject(name=''):
    if os.path.exists('database'):
        os.chdir('database')
    saves = []
    for entry in os.listdir(os.getcwd()):
        if entry.find('.chris') > 0 and entry.find(name) > -1:
            saves.append(entry[0:entry.index('.chris')])
    return saves


# Prints the result of get_saves
def dispayNamesOfSavesForProject(name=''):
    saves = listNamesOfSavesForProject(name)
    saves.sort()
    saves.reverse()
    for save in saves:
        print(save)


# Given the name of the project
# Finds the chris files with this project name
# Records the names of those chris files
# Returns the highest save number in those names
# Returns -1 if no chris file of this project was found
def findRecentSaveForProject(name=''):
    num = -1
    for save in listNamesOfSavesForAProject(name):
        save_num = int(save[save.rindex('-') + 1:])
        if save_num > num:
            num = save_num
    return num


# Given the name of the project and the location of the project
# Records the most recent save number
# Creates a new chris file of the project
def createSaveForProjectAtPath(name='', project_path=""):
    num = findRecentSaveForProject(name)
    previous = num
    if num == -1:
        previous = 'None'
    ChrisFileManager.ChrisWriter(name, project_path).writeChrisFile(num + 1, previous)


# Given a save name and a location to create the project
# Creates the project based off the corresponding chris file
def recreateSaveOfProjectAtPath(save='', target_path=''):
    os.chdir('database')
    save_file = save + '.chris'
    if save_file in os.listdir(os.getcwd()):
        target = os.path.join(os.getcwd(), save_file)
        ChrisFileManager.ChrisReader(target).recreateProject(target_path)
    else:
        print('INVALID SAVE')


# Given the save of a file and a list of the other saves
# Returns true if this save of a file is used by another save, false if not
def checkFileIsUsed(file="", version="", remaining_saves=None):
    for dif_save in remaining_saves:
        dif_save_file = dif_save + '.chris'
        if file in ChrisFileManager.ChrisReader(dif_save_file).files.keys():
            if ChrisFileManager.ChrisReader(dif_save_file).file_data[file] == version:
                return True
    return False


# Given the save name
# Records the other saves of the project
# Checks every file described by the chris file of this save name
# Removes the file if it not used by another save
def removeUnusedFiles(save=''):
    name = save[0:save.rindex('-')]
    remaining_saves = get_saves(name)
    remaining_saves.remove(save)
    save_file = save + '.chris'
    files = ChrisFileManager.ChrisReader(save_file).files.keys()
    for entry in files:
        version = ChrisFileManager.ChrisReader(save_file).file_data[entry]
        used = checkFileIsUsed(entry, version, remaining_saves)
        if not used:
            version_file = entry[0:entry.rindex('.')] + '-' + str(version) + entry[entry.rindex('.'):]
            if os.path.exists(version_file):
                os.remove(version_file)


# Given the save name
# If the database folder is not already accessed, accesses the database folder
# Checks if a chris file with this save name exists
# Removes this chris file and its unused files
def deleteSaveOfThisName(save=''):
    if os.path.exists('database'):
        os.chdir('database')
    save_file = save + '.chris'
    if not os.path.exists(save_file):
        print('INVALID SAVE')
    if os.path.exists(save_file):
        removeUnusedFiles(save)
        os.remove(save_file)


# Given the name of the project and the location of the project
# Deletes the most recent chris file save
# Creates a new chris file of the project
def deleteRecentSaveAndCreateNewSave(name='', project_path=''):
    num = get_recent_save(name)
    if num == -1:
        new_save(name, project_path)
    else:
        recent_save = name + '-' + str(num)
        delete_save(recent_save)
        new_save(name, project_path)


# Prints the ChrisVCS-instructions
def showInstructions():
    os.chdir('database')
    instructions = open('ChrisVCS-instructions.txt').readlines()
    for line in instructions:
        print(line)


# Terminal Commands
def commands():
    if len(sys.argv) == 2:
        if sys.argv[1] == 'show_projects':
            displayNamesOfExistingProjects()
        elif sys.argv[1] == 'show_instructions':
            showInstructions()
        else:
            print('INVALID COMMAND')
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'show_saves':
            dispayNamesOfSavesForAProject(sys.argv[2])
        elif sys.argv[1] == 'delete_save':
            deleteSaveOfThisName(sys.argv[2])
        else:
            print('INVALID COMMAND')
    elif len(sys.argv) == 4:
        if sys.argv[1] == 'new_project':
            createNewProjectAtPath(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'new_save':
            createSaveForProjectAtPath(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'load_save':
            recreateSaveOfProjectAtPath(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'quick_save':
            deleteRecentSaveAndCreateNewSave(sys.argv[2], sys.argv[3])
        else:
            print('INVALID COMMAND')
    else:
        print('INVALID ARGUMENTS')


if __name__ == '__main__':
    commands()
