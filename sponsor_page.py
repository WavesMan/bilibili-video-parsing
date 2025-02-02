import tkinterweb
import customtkinter as ctk

class SponsorPage:
    def __init__(self, root):
        self.root = root
        self.create_sponsor_page()

    def create_sponsor_page(self):
        """创建赞助页面，加载网页内容"""
        self.clear_page()
        
        # 创建一个 HtmlFrame 来加载网页
        self.web_frame = tkinterweb.HtmlFrame(self.root, width=960, height=500)
        self.web_frame.load_url("http://dq.foreve.asia")  # 加载网页
        self.web_frame.pack(fill="both", expand=True)

    def clear_page(self):
        """清空页面内容（保留菜单栏）"""
        for widget in self.root.winfo_children():
            if not isinstance(widget, ctk.CTkFrame):  # 保留菜单栏（假设菜单栏是 CTkFrame）
                widget.destroy()