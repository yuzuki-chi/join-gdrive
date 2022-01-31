import os
import re
import shutil

BASE_FILE_PATH = "/<google-drive-download-dir>"
TARGET_DIR_NAME = "<dir name>"
OUTPUT_DIR_PATH = BASE_FILE_PATH + "/output"


##
# BASE_FILE_PATH : 分割されたディレクトリの親ディレクトリを指定  ;e.g. /downloads/input/dir 1  /input/dir 2 であれば /downloads/input
# TARGET_DIR_NAME: 分割されたディレクトリ名                   ;e.g. /download/input/dir 1 /dir/dir 2 であれば dir
# OUTPUT_DIR_PATH: 特に指定なし
##

class Entry:
    file_name: str
    BASE_FILE_PATH: str
    file_hierarchy: str
    file_path: str
    file_full_path: str

    def __init__(self, file_path):
        self.file_full_path = file_path
        self.file_name = re.search("([^/]+?)?$", file_path).group()
        self.file_hierarchy = file_path.split('/')
        if self.file_hierarchy[0] == "":  # root dir
            self.file_hierarchy[0] = "/"

        self.file_path = self.file_full_path.replace(BASE_FILE_PATH, "")
        if self.file_path == "":  # root dir
            self.file_path = "/"

        # print(self.file_full_path + " => " + self.file_path)

        if self.file_path.count("/") == 1:  # TODO: 分割に含まれずそのままダウンロードされたファイルは対象外となっている.
            # print("[parent]" + self.file_path)
            pass
        else:  # 対象となる子ディレクトリ
            self.file_path = re.match('/[^/]+/(.+)', self.file_path).group(1)

    def get_file_name(self):
        return self.file_name

    def get_file_full_path(self):
        return self.file_full_path

    def get_file_path(self):
        return self.file_path

    def get_file_hierarchy(self):
        return self.file_hierarchy


def get_file_type(file_path: str = "") -> int:
    # 0:unknown, 1:file, 2:dir
    if os.path.isdir(file_path):
        return 2
    elif os.path.isfile(file_path):
        return 1
    else:
        return 0


def dig_dir(entry: Entry):
    for target in entry:
        file_type = get_file_type(target.get_file_full_path())

        # dir
        if file_type == 2:
            entry = []
            for e in os.listdir(path=target.get_file_full_path()):
                entry.append(Entry(target.get_file_full_path() + "/" + e))
            dig_dir(entry)  # 再帰

        # file
        elif file_type == 1:
            pass
            # print(target.get_file_full_path() + " -> " + OUTPUT_DIR_PATH + "/" + target.get_file_path())
            copy_file(target.get_file_full_path(), OUTPUT_DIR_PATH + "/" + target.get_file_path())

        # other file
        else:
            print("[ERR]\t" + target.get_file_full_path() + " is not file")


def copy_file(source: str, target: str):
    print(source)
    print(target)
    if not os.path.exists(os.path.dirname(target)):
        os.makedirs(os.path.dirname(target))
        print("[log] \tCreate new directory: " + os.path.dirname(target))
    shutil.copy2(source, target)


if __name__ == '__main__':

    # Parent Entry
    file = Entry(BASE_FILE_PATH)

    # Create Entry list -------------------------------------------
    entry = []
    for e in os.listdir(path=BASE_FILE_PATH):
        entry.append(Entry(BASE_FILE_PATH + "/" + e))

    # Create subject dir ------------------------------------------
    subject_dir = []
    for e in entry:
        if TARGET_DIR_NAME in e.get_file_name():
            subject_dir.append(e)

    # Create output dir -------------------------------------------
    if not os.path.exists(OUTPUT_DIR_PATH):
        os.makedirs(OUTPUT_DIR_PATH)
    else:
        print("[WARN]\t" + OUTPUT_DIR_PATH + " is already exists.")

    # Start dig
    print("Join file ...")
    dig_dir(subject_dir)
