一个用于自动化创建树莓派pico项目（C++项目）的小脚本。需要按照官方指导设置好pico开发环境，包括：
 - 安装指定的交叉编译工具链（arm gcc）
 - 下载（或git clone）pico sdk
 - 设置PICO_SDK_PATH等关键的环境变量
 - ...

make_project.py：以命令行形式引导用户输入项目目录、项目名称等信息，然后创建项目。

make_project_gui.py：以简单的图形界面引导用户输入相关信息，然后创建项目。


