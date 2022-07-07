import easygui
import pyperclip

from make_project import *


def select_project_dir(default_dir):
    should_select = easygui.ccbox("将在'{}'创建项目".format(default_dir), choices=["选择其他目录", "下一步"])
    if should_select:
        # 打开目录选择对话框选择一个目录
        selected_dir = easygui.diropenbox("选择项目路径", "选择项目路径", default_dir)
        if selected_dir is None or selected_dir == "":
            selected_dir = default_dir
        # 递归，等待用户最终确认
        return select_project_dir(selected_dir)
    else:
        return default_dir


def input_project_name():
    return easygui.enterbox("请输入项目名称", "项目名称", default=DEFAULT_PROJECT_NAME, strip=True)


def confirm(project_name, project_path):
    msg = """
    项目名称：{}
    项目路径：{}
    """.format(project_name, project_path)
    return easygui.ccbox(msg, "创建项目", choices=["确认创建", "取消"])


if __name__ == '__main__':
    project_dir = select_project_dir(DEFAULT_PROJECT_DIR)
    if not os.path.isdir(project_dir):
        print("非法项目路径：{}".format(project_dir))
        easygui.msgbox("非法的路径，请选择正确的路径！({})".format(project_dir), "错误")
        exit(1)
    project_name = input_project_name()
    if project_name is None:
        # 用户取消了创建，直接退出
        print("用户取消项目创建！")
        exit(0)
    if project_name == "":
        print("非法的项目名称：{}".format(project_name))
        easygui.msgbox("非法的项目名称，项目名称不可为空！", "错误")
        exit(1)
    project_path = os.path.abspath(os.path.join(project_dir, project_name))
    if os.path.isdir(project_path) and len(os.listdir(project_path)) != 0:
        print("项目目录已存在且不为空: {}".format(project_path))
        easygui.msgbox("项目目录已存在且不为空！({})".format(project_path), "错误")
        exit(1)
    if confirm(project_name, project_path):
        try:
            print("开始创建项目...")
            # 创建项目目录
            if not os.path.isdir(project_path):
                print("创建项目目录...")
                os.makedirs(project_path, exist_ok=True)
            # 复制源码文件目录到工程目录
            print("复制源码...")
            shutil.copytree(SRC_DIR, os.path.join(project_path, "src"))
            # 检测pico_sdk_import.cmake路径
            pico_sdk_import_cmake_path = detect_pico_sdk_import_cmake()
            # 复制pico_sdk_import.cmake文件
            print("复制pico_sdk_import.cmake文件(来源：{})...".format(pico_sdk_import_cmake_path))
            shutil.copy(pico_sdk_import_cmake_path, project_path)
            # 生成CMakeLists.txt文件
            print("生成CMakeLists.txt文件...")
            with open(os.path.join(project_path, "CMakeLists.txt"), "w") as f:
                f.write(generate_cmakelists(project_name))
            # 创建成功，提示用户
            print("项目创建完成！")
            copy_project_path = easygui.ccbox("项目创建成功：{}".format(project_path), choices=["复制项目路径", "退出"])
            if copy_project_path:
                pyperclip.copy(project_path)
                print("项目路径已拷贝到剪贴板！")
            exit(0)
        except Exception as e:
            easygui.msgbox("创建项目过程中发生一个异常：".format(e), "错误")
            exit(1)
