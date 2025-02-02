import customtkinter as ctk
import requests  # 导入 requests 库
import webbrowser

class AboutPage:
    def __init__(self, root):
        self.root = root
        self.current_version = "v1.1.0"  # 当前版本
        self.create_about_page()

    def create_about_page(self):
        """创建关于页面"""
        self.clear_page()

        # 创建关于界面的主框架
        self.about_frame = ctk.CTkFrame(self.root)
        self.about_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 标题
        about_label = ctk.CTkLabel(
            self.about_frame,
            text="关于本应用程序",
            font=("SimHei", 16, "bold")
        )
        about_label.pack(pady=10)

        # 第一栏：当前程序版本
        version_label = ctk.CTkLabel(
            self.about_frame,
            text=f"当前程序版本: {self.current_version}",
            font=("SimHei", 14)
        )
        version_label.pack(pady=5, fill="x")

        # 第二栏：开发者信息（可点击）
        developer_button = ctk.CTkButton(
            self.about_frame,
            text="开发者: GitHub@WavesMan",
            font=("SimHei", 14),
            fg_color="transparent",
            border_width=0,
            text_color=("white"),
            command=self.open_developer_github
        )
        developer_button.pack(pady=5, fill="x")

        # 第三栏：仓库地址（可点击）
        repo_frame = ctk.CTkFrame(self.about_frame, fg_color="transparent")
        repo_frame.pack(pady=5, fill="x")

        repo_text_label = ctk.CTkLabel(
            repo_frame,
            text="仓库地址:",
            font=("SimHei", 14)
        )
        repo_text_label.pack(anchor="center")

        repo_button = ctk.CTkButton(
            self.about_frame,
            text="https://github.com/WavesMan/bilibili-video-parsing",
            font=("SimHei", 14),
            fg_color="transparent",
            border_width=0,
            text_color=("white"),
            command=self.open_repo_github
        )
        repo_button.pack(pady=5, fill="x")

        # 第四栏：检查更新（可点击）
        check_update_button = ctk.CTkButton(
            self.about_frame,
            text="检查更新",
            font=("SimHei", 14),
            command=self.check_for_updates
        )
        check_update_button.pack(pady=5, fill="x")

    def check_for_updates(self):
        """检查更新"""
        try:
            response = requests.get("https://api.github.com/repos/WavesMan/bilibili-video-parsing/releases/latest")
            response.raise_for_status()
            latest_release = response.json()
            latest_version = latest_release['tag_name']
            download_url = latest_release['html_url']

            if latest_version != self.current_version:
                self.display_update_info(latest_version, download_url)
            else:
                self.show_message("当前已是最新版本！")

        except Exception as e:
            self.show_message(f"检查更新失败：{str(e)}")

    def display_update_info(self, latest_version, download_url):
        """显示更新信息"""
        update_info_label = ctk.CTkLabel(
            self.about_frame,
            text=f"最新版本: {latest_version}",
            font=("SimHei", 14)
        )
        update_info_label.pack(pady=5, fill="x")

        download_button = ctk.CTkButton(
            self.about_frame,
            text="前往下载更新",
            font=("SimHei", 14),
            command=lambda: webbrowser.open(download_url)
        )
        download_button.pack(pady=5, fill="x")

    def show_message(self, message):
        """显示消息"""
        message_label = ctk.CTkLabel(
            self.about_frame,
            text=message,
            font=("SimHei", 14)
        )
        message_label.pack(pady=5, fill="x")

    def open_developer_github(self):
        webbrowser.open("https://github.com/WavesMan")

    def open_repo_github(self):
        webbrowser.open("https://github.com/WavesMan/bilibili-video-parsing")  # 打开指定的GitHub页面

    def get_latest_version(self):
        """获取最新版本"""
        # 这里可以添加获取最新版本的逻辑
        print("获取最新版本")

    def clear_page(self):
        """清空页面内容（保留菜单栏）"""
        for widget in self.root.winfo_children():
            if not isinstance(widget, ctk.CTkFrame):  # 保留菜单栏（假设菜单栏是 CTkFrame）
                widget.destroy()
