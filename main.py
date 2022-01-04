import os
import re


class Entry:
    file_name: str
    BASE_FILE_PATH: str
    file_hierarchy: str

    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = re.search("([^/]+?)?$", file_path).group()
        self.file_hierarchy = file_path.split('/')
        if self.file_hierarchy[0] == "":  # root dir
            self.file_hierarchy[0] = "/"

    def get_file_name(self):
        return self.file_name

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
        file_type = get_file_type(target.get_file_path())
        # TODO: dirの時は再起的にディレクトリを作成し, fileの時はファイルデータをコピーする
        # dir
        if file_type == 2:
            # print(target.get_file_path() + " is dir!")
            # output_dirname = target.get_file_path()
            entry = []
            for e in os.listdir(path=target.get_file_path()):
                entry.append(Entry(target.get_file_path() + "/" + e))
            dig_dir(entry)  # 再帰

        # file
        elif file_type == 1:
            print(target.get_file_hierarchy())
            print(target.get_file_path() + " is file")

        else:
            print("[ERR]\t" + target.get_file_path() + " is not file")


BASE_FILE_PATH = "/Users/yuzukichi/Downloads/NOT_SYNC"
OUTPUT_DIR_PATH = BASE_FILE_PATH + "/output/NOT_SYNC"

if __name__ == '__main__':

    file = Entry(BASE_FILE_PATH)

    entry = []
    for e in os.listdir(path=BASE_FILE_PATH):
        entry.append(Entry(BASE_FILE_PATH + "/" + e))

    # JOINするNOT_SYNCをリストアップ
    subject_dir = []
    for e in entry:
        if "NOT_SYNC" in e.get_file_name():
            subject_dir.append(e)
            # print(subject_dir[-1].get_file_path())

    # output/NOT_SYNC/ の作成
    if not os.path.exists(OUTPUT_DIR_PATH):
        os.makedirs(OUTPUT_DIR_PATH)
    else:
        print("[WARN]\t" + OUTPUT_DIR_PATH + " is already exists.")

    dig_dir(subject_dir)
