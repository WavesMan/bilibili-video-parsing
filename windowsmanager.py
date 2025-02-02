import customtkinter as ctk
from sponsor_page import SponsorPage
from about_page import AboutPage
import get_bilibili_stream  # 导入 get_bilibili_stream.py
import pyperclip  # 导入 pyperclip 用于剪切板操作

class WindowsManager:
    def __init__(self, root):
        self.root = root
        self.bvid = None
        self.urls = []  # 用于存储解析得到的 URL
        self.set_font()
        self.create_menu()
        self.create_main_interface()

    def set_font(self):
        self.custom_font = ctk.CTkFont(family="SimHei", size=15)
        self.menu_font = ctk.CTkFont(family="SimHei", size=14)

    def create_menu(self):
        self.menubar = ctk.CTkFrame(self.root, height=40)
        self.menubar.pack(side="top", fill="x")

        # 添加“功能”按钮
        self.function_button = ctk.CTkButton(
            self.menubar,
            text="功能",
            font=self.menu_font,
            command=self.create_main_interface,
            width=100,
            height=30
        )
        self.function_button.pack(side="left", padx=10, pady=5)

        # 添加“赞助”按钮
        self.sponsor_button = ctk.CTkButton(
            self.menubar,
            text="赞助",
            font=self.menu_font,
            command=self.show_sponsor_page,
            width=100,
            height=30
        )
        self.sponsor_button.pack(side="left", padx=10, pady=5)

        # 添加“关于”按钮
        self.about_button = ctk.CTkButton(
            self.menubar,
            text="关于",
            font=self.menu_font,
            command=self.show_about_page,
            width=100,
            height=30
        )
        self.about_button.pack(side="left", padx=10, pady=5)

    def create_main_interface(self):
        self.clear_interface()

        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.main_label = ctk.CTkLabel(
            self.main_frame,
            text="请输入 Bilibili 视频的 BV 号：",
            font=self.custom_font
        )
        self.main_label.pack(pady=10)

        self.bvid_entry = ctk.CTkEntry(
            self.main_frame,
            font=self.custom_font,
            width=300,
            placeholder_text="例如：BV1xx411c7mD"
        )
        self.bvid_entry.pack(pady=10)

        self.parse_button = ctk.CTkButton(
            self.main_frame,
            text="解析视频",
            font=self.custom_font,
            command=self.parse_video,
            width=100,
            height=30
        )
        self.parse_button.pack(pady=10)

        self.output_textbox = ctk.CTkTextbox(
            self.main_frame,
            font=self.custom_font,
            width=440,
            height=220,
            wrap="word"
        )
        self.output_textbox.pack(pady=10)
        self.output_textbox.insert("1.0", "解析结果将显示在这里...")
        self.output_textbox.configure(state="disabled")

        # 添加“复制”按钮
        self.copy_button = ctk.CTkButton(
            self.main_frame,
            text="复制解析链接",
            font=self.custom_font,
            command=self.copy_to_clipboard,
            width=100,
            height=30
        )
        self.copy_button.pack(pady=10)

    def parse_video(self):
        """解析视频"""
        self.bvid = self.bvid_entry.get().strip()

        if not self.bvid:
            self.output_textbox.configure(state="normal")
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("1.0", "错误：请输入有效的 BV 号！")
            self.output_textbox.configure(state="disabled")
            return

        # 调用 get_bilibili_stream.py 中的 get_video_urls 函数
        try:
            self.urls = get_bilibili_stream.get_video_urls(self.bvid)  # 存储解析得到的 URL
            output_text = "解析成功！\nBV 号：{}\n视频地址：\n{}\n".format(self.bvid, "\n".join(self.urls))
        except Exception as e:
            output_text = f"解析失败：{str(e)}"

        self.output_textbox.configure(state="normal")
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("1.0", output_text)
        self.output_textbox.configure(state="disabled")

    def copy_to_clipboard(self):
        """将 URL 复制到剪切板"""
        if not self.urls:
            self.output_textbox.configure(state="normal")
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("1.0", "错误：没有可复制的 URL！")
            self.output_textbox.configure(state="disabled")
            return
        
        # 复制所有 URL 到剪切板
        urls_to_copy = "\n".join(self.urls)
        pyperclip.copy(urls_to_copy)  # 使用 pyperclip 进行复制
        self.output_textbox.configure(state="normal")
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("1.0", "URL 已复制到剪切板！")
        self.output_textbox.configure(state="disabled")

    def show_sponsor_page(self):
        self.clear_interface()
        SponsorPage(self.root)

    def show_about_page(self):
        self.clear_interface()
        AboutPage(self.root)

    def clear_interface(self):
        for widget in self.root.winfo_children():
            if widget != self.menubar:
                widget.destroy()
