import os
import shutil

DEFAULT_PROJECT_DIR = os.getcwd()
DEFAULT_PROJECT_NAME = "pico_blink"
CURRENT_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(CURRENT_DIR, "project_template")
SRC_DIR = os.path.join(TEMPLATE_DIR, "src")
PICO_SDK_PATH = os.environ.get("PICO_SDK_PATH")
PICO_SDK_IMPORT_CMAKE_FILENAME = "pico_sdk_import.cmake"
CMAKELISTS_TEMPLATE = os.path.join(TEMPLATE_DIR, "CMakeLists.txt")


def detect_pico_sdk_import_cmake():
    """
    通过PICO_SDK_PATH环境变量寻找“pico_sdk_import.cmake”文件，若未找到则使用本目录下默认的pico_sdk_import.cmake
    :return:  pico_sdk_init.cmake文件的路径
    """
    if PICO_SDK_PATH is None or PICO_SDK_PATH == "":
        pico_sdk_import_cmake_file = os.path.join(os.path.dirname(__file__), PICO_SDK_IMPORT_CMAKE_FILENAME)
    else:
        pico_sdk_import_cmake_file = os.path.join(PICO_SDK_PATH, "external/", PICO_SDK_IMPORT_CMAKE_FILENAME)
        if not os.path.isfile(pico_sdk_import_cmake_file):
            pico_sdk_import_cmake_file = os.path.join(os.path.dirname(__file__), PICO_SDK_IMPORT_CMAKE_FILENAME)
    return pico_sdk_import_cmake_file


def generate_cmakelists(project_name):
    """
    生成CMakeList.txt文件内容
    :param project_name: 工程名称
    :return:
    """
    with open(CMAKELISTS_TEMPLATE, "r") as f:
        template = f.read()
    generated = template.replace("$$PROJECT_NAME$$", project_name)
    return generated


if __name__ == '__main__':
    # 先获取工程目录所在的路径
    project_dir = input("请输入工程目录所在路径（默认在当前工作目录创建工程目录）：")
    if project_dir == "":
        # 默认在当前工作目录下创建工程目录
        project_dir = DEFAULT_PROJECT_DIR
    # 若输入的路径并非一个已存在的目录，则报错推出
    if not os.path.isdir(project_dir):
        print("错误：指定目录不存在，请手动创建该目录（{}）".format(project_dir))
        exit(1)
    # 获取工程名称
    project_name = input("请输入工程名称（默认为pico_blink）:")
    if project_name == "":
        project_name = DEFAULT_PROJECT_NAME
    # 生成目标工程完整路径
    project_path = os.path.abspath(os.path.join(project_dir, project_name))
    # 检查目录是否已存在
    if os.path.isdir(project_path) and len(os.listdir(project_path)) != 0:
        print("错误：工程目录已存在且不为空（{}）".format(project_path))
        exit(1)
    print("工程目录路径为：{}".format(project_path))
    print("正在创建工程...")
    # 目录不存在则创建目录
    print("正在复制源码...")
    if not os.path.isdir(project_path):
        os.makedirs(project_path, exist_ok=True)
    # 复制源码文件目录到工程目录
    shutil.copytree(SRC_DIR, os.path.join(project_path, "src"))
    # 检测pico_sdk_import.cmake路径
    pico_sdk_import_cmake_path = detect_pico_sdk_import_cmake()
    print("正在复制pico_sdk_import.cmake文件（来源：{}）...".format(pico_sdk_import_cmake_path))
    shutil.copy(pico_sdk_import_cmake_path, project_path)
    print("正在生成CMakeLists.txt文件...")
    with open(os.path.join(project_path, "CMakeLists.txt"), "w") as f:
        f.write(generate_cmakelists(project_name))
    print("项目创建成功（{}）！".format(project_path))
