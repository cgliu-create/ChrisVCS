import os
import sys


def format_save_of_file(file="", save=""):
    return file[0: file.find('.')] + '-' + save + file[file.find('.'):]


class ChrisWriter:
    def __init__(self, project='', path='', ):
        self.project = project
        self.path = path
        self.folders = {}
        self.files = {}
        self.file_data = {}

    # Given a path to a directory
    # Records internal directories in that directory
    def record_folders(self, path=''):
        folder_name_path_list = {}
        for entry in os.scandir(path):
            if os.path.isdir(entry):
                folder_name_path_list[entry.name] = os.path.relpath(entry.path, self.path)
        return folder_name_path_list

    # Given a path to a directory
    # Records files in that directory
    # Does not record files that are in an internal directory
    def record_files(self, path=''):
        file_name_path_list = {}
        for entry in os.scandir(path):
            if os.path.isfile(entry) and entry.name != '.DS_Store':
                file_name_path_list[entry.name] = os.path.relpath(entry.path, self.path)
        return file_name_path_list

    # Given a path to a directory
    # Records and opens every internal directory
    # Records all files
    def record_project(self, path=''):
        files = self.record_files(path)
        for entry in files:
            self.files[entry] = files[entry]
        folders = self.record_folders(path)
        if len(folders) >= 1:
            for entry in folders:
                self.folders[entry] = folders[entry]
                self.record_project(os.path.join(self.path, folders[entry]))

    # Given the new save name and previous save name
    # Goes through files
    # Finds the most recent save of a file
    # Compares the current file to the save
    # if there is a change, creates and records a new save
    # if it is unchanged, records the old save
    def save_files(self, name='0', previous='None'):
        for entry in self.files:
            path = os.path.join(self.path, self.files[entry])
            save_content = cur_content = open(path).readlines()
            recent_save = new_save = format_save_of_file(entry, name)
            unique = True
            if previous != 'None':
                recent = int(previous)
                found = False
                while not found:
                    recent_save = format_save_of_file(entry, str(recent))
                    if os.path.exists(recent_save):
                        save_content = open(recent_save).readlines()
                        found = True
                    elif recent < 0:
                        recent_save = new_save
                        found = True
                    else:
                        recent -= 1
                if save_content == cur_content:
                    unique = False
            if unique:
                self.file_data[entry] = new_save
                open(new_save, 'x').writelines(cur_content)
            else:
                self.file_data[entry] = recent_save
                if not os.path.exists(recent_save):
                    open(recent_save, 'x').writelines(save_content)

    # Given the new save name and previous save name
    # Records directories and files inside
    # Records the save of the most recent change for a file
    def write_chris_file(self, name='0', previous='None'):
        self.record_project(self.path)
        self.save_files(name, previous)
        chris = open(self.project + '-' + name + '.chris', 'at')
        chris.write(self.project + '\n')
        chris.write(name + '\n')
        chris.write(previous + '\n')
        chris.write(str(len(self.folders)) + '\n')
        for entry in self.folders:
            path = self.folders[entry]
            chris.write(entry + ':' + path[0:path.find(entry)] + '\n')
        chris.write(str(len(self.files)) + '\n')
        for entry in self.files:
            path = self.files[entry]
            save = self.file_data[entry]
            chris.write(entry + ':' + path[0:path.find(entry)] + ':' + save[save.find('-') + 1:save.find('.')] + '\n')
        chris.close()


def remove_newline_char(line=""):
    return line[0: line.find('\n')]


class ChrisReader:
    def __init__(self):
        self.project = ""
        self.name = ""
        self.previous = ""
        self.folders = {}
        self.files = {}
        self.file_data = {}

    # Records info on saves, folders, and files
    def read_chris_file(self, path=''):
        content = open(path).readlines()
        self.project = remove_newline_char(content[0])
        self.name = remove_newline_char(content[1])
        self.previous = remove_newline_char(content[2])
        folder_num = int(remove_newline_char(content[3]))
        start = 4
        end = start + folder_num
        for i in range(start, end):
            folder_info = remove_newline_char(content[i])
            folder_name = folder_info[0:folder_info.find(':')]
            folder_location = folder_info[folder_info.find(':') + 1:]
            self.folders[folder_name] = folder_location
        file_num = int(remove_newline_char(content[end]))
        start = end + 1
        end = start + file_num
        for i in range(start, end):
            file_info = remove_newline_char(content[i])
            file_name = file_info[0:file_info.find(':')]
            file_info = file_info[file_info.find(':') + 1:]
            file_location = file_info[0:file_info.find(':')]
            file_version = file_info[file_info.find(':') + 1:]
            self.files[file_name] = file_location
            self.file_data[file_name] = file_version

    # Creates folders and files based on recorded info
    def recreate_project(self, targetpath=""):
        path = os.path.join(targetpath, self.project)
        os.mkdir(path)
        for entry in self.folders:
            rel_path = self.folders[entry] + entry
            folder_path = os.path.join(path, rel_path)
            os.mkdir(folder_path)
        for entry in self.files:
            rel_path = self.files[entry] + entry
            file_path = os.path.join(path, rel_path)
            save = self.file_data[entry]
            save_file = format_save_of_file(entry, save)
            content = open(save_file).readlines()
            open(file_path, 'x').writelines(content)

