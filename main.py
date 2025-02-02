import customtkinter as ctk
from windowsmanager import WindowsManager

class MainApplication:
    def __init__(self):
        # 初始化主窗口
        self.root = ctk.CTk()
        self.root.title("BiliBili Video Parsing")
        self.root.geometry("960x540")

        # 初始化窗口管理模块
        self.windows_manager = WindowsManager(self.root)

        # 启动主界面
        self.windows_manager.create_main_interface()

    def run(self):
        # 启动主事件循环
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApplication()
    app.run()