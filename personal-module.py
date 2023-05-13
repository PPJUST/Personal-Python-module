# 文件操作类
def get_all_files_under_folder(folder: str) -> list:
    """获取文件夹下的所有文件路径

    输入：folder

    folder：目标文件夹路径，str类型

    返回：all_files

    all_files：所有文件路径，list类型
    """
    import os
    all_files = []
    for root, directories, files in os.walk(folder):
        for filename in files:
            # 获取每个文件的完整路径，并添加到列表中
            file_path = os.path.join(root, filename)
            file_path = file_path.replace('/', '\\')  # 替换路径中不同的斜杠
            all_files.append(file_path)
    return all_files


def find_first_folder_with_multiple_files(folder: str) -> str:
    """找出文件夹中第一个含多个文件/文件夹的文件夹，用于处理嵌套文件夹

    输入：folder

    folder：目标文件夹路径，str类型

    返回：first_folder

    first_folder：符合条件的文件夹路径，str类型
    """
    import os
    if len(os.listdir(folder)) == 1:
        if os.path.isfile(os.path.join(folder, os.listdir(folder)[0])):  # 如果文件夹下只有一个文件，并且是文件
            first_folder = os.path.join(folder, os.listdir(folder)[0])
            return first_folder
        else:
            return find_first_folder_with_multiple_files(
                os.path.join(folder, os.listdir(folder)[0]))  # 临时文件夹下只有一个文件，但是文件夹，则递归
    else:
        first_folder = folder
        return first_folder


def rename_without_duplication(filepath: str, folder: str) -> str:
    """递归重命名，直到目标文件夹下没有与该文件重名

    输入：filepath, folder

    filepath：目标文件路径，str类型

    folder：目标文件夹路径，str类型

    返回：new_filename

    new_filename：新的文件名，str类型
    """
    import os
    filetitle = os.path.split(os.path.splitext(filepath)[0])[1]
    suffix = os.path.splitext(filepath)[1]
    count = 1
    all_filename = os.listdir(folder) + os.listdir(os.path.split(filepath)[0])
    all_filename = [x.upper() for x in all_filename]  # 转大写，防止大小写匹配不到
    while True:
        new_filename = f"{filetitle} - new{count}{suffix}"
        if new_filename.upper() not in all_filename:
            return new_filename
        else:
            count += 1


def is_zip_file(filepath: str) -> bool:
    """检查文件是否是压缩包

    输入：filepath

    filepath:目标文件路径，str类型

    返回：bool值
    """
    import magic
    zip_type = ['application/x-rar', 'application/x-gzip', 'application/x-tar', 'application/zip',
                'application/x-lzh-compressed', 'application/x-7z-compressed', 'application/x-xz',
                'application/octet-stream', 'application/x-dosexec']
    file_type = magic.from_buffer(open(filepath, 'rb').read(2048), mime=True)
    if file_type in zip_type:
        return True
    else:
        return False


def get_zip_title(filepath: str) -> str:
    """提取文件名

    输入：filepath

    filepath:目标文件路径，str类型

    返回：zip_name

    zip_name:提取的文件名（不含后缀），如果不符合正则返回空，str类型
    """
    import re
    import os
    filename = os.path.split(filepath)[1]
    re_rar = r"^(.+)\.part\d+\.rar$"  # 4种压缩文件的命名规则
    re_7z = r"^(.+)\.7z\.\d+$"
    re_zip_first = r"^(.+)\.zip$"
    re_zip_other = r"^(.+)\.z\d+$"
    if re.match(re_7z, filename):
        zip_name = re.match(re_7z, filename).group(1)
    elif re.match(re_zip_first, filename):
        zip_name = re.match(re_zip_first, filename).group(1)
    elif re.match(re_rar, filename):
        zip_name = re.match(re_rar, filename).group(1)
    elif re.match(re_zip_other, filename):
        zip_name = re.match(re_zip_other, filename).group(1)
    else:
        zip_name = ''
    return zip_name


def get_files_size(filepaths: list) -> int:
    """获取输入文件的总大小

    输入：filepaths

    filepaths：文件路径的列表，list类型

    返回：total_size

    total_size：输入文件的总大小（byte），int类型
    """
    import os
    total_size = 0
    for file in filepaths:
        total_size += os.path.getsize(file)
    return total_size


def get_folder_size(folder: str) -> int:
    """获取输入文件夹的总大小

    输入：folder

    folder：文件夹路径，str类型

    返回：total_size

    total_size：文件夹的大小（byte），int类型
    """
    import os
    folder_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for item in filenames:
            filepath = os.path.join(dirpath, item)
            folder_size += os.path.getsize(filepath)
    return folder_size


def is_hidden(path: str) -> bool:
    """检查文件是否隐藏

    输入：path

    path：文件/文件夹路径，str类型

    返回：bool值
    """
    import ctypes

    # 定义WinAPI函数
    GetFileAttributesW = ctypes.windll.kernel32.GetFileAttributesW

    # 定义常量
    FILE_ATTRIBUTE_HIDDEN = 0x2
    INVALID_FILE_ATTRIBUTES = -1

    def check(file):
        # 获取文件属性
        attrs = GetFileAttributesW(file)
        if attrs == INVALID_FILE_ATTRIBUTES:
            # 文件不存在或无法访问
            return False
        return attrs & FILE_ATTRIBUTE_HIDDEN == FILE_ATTRIBUTE_HIDDEN

    return check(path)


# 其他
def get_time(style: str = '%Y-%m-%d %H:%M:%S') -> str:
    """获取结构化的当前时间

    输入：style

    style：时间结构，有默认值，str类型

    返回：结构化的当前时间
    """
    import time
    return time.strftime(style, time.localtime())
