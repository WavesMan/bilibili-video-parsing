# gui.py
import customtkinter as ctk
import tkinterweb
import requests
import json
import sys
import webbrowser
import pyperclip

class MainApplication:
    def __init__(self):
        # Initialize main window
        self.root = ctk.CTk()
        self.root.title("BiliBili Video Parsing")
        self.root.geometry("960x540")

        # Initialize window manager
        self.windows_manager = WindowsManager(self.root)

        # Launch main interface
        self.windows_manager.create_main_interface()

    def run(self):
        # Start main event loop
        self.root.mainloop()

class WindowsManager:
    def __init__(self, root):
        self.root = root
        self.bvid = None
        self.urls = []  # To store parsed URLs
        self.set_font()
        self.create_menu()

    def set_font(self):
        self.custom_font = ctk.CTkFont(family="SimHei", size=15)
        self.menu_font = ctk.CTkFont(family="SimHei", size=14)

    def create_menu(self):
        self.menubar = ctk.CTkFrame(self.root, height=40)
        self.menubar.pack(side="top", fill="x")

        # Add buttons to the menu
        self.function_button = ctk.CTkButton(
            self.menubar,
            text="功能",
            font=self.menu_font,
            command=self.create_main_interface,
            width=100,
            height=30
        )
        self.function_button.pack(side="left", padx=10, pady=5)

        self.sponsor_button = ctk.CTkButton(
            self.menubar,
            text="赞助",
            font=self.menu_font,
            command=self.show_sponsor_page,
            width=100,
            height=30
        )
        self.sponsor_button.pack(side="left", padx=10, pady=5)

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

        # Add "Copy" button
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
        """Parse video"""
        self.bvid = self.bvid_entry.get().strip()

        if not self.bvid:
            self.output_textbox.configure(state="normal")
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("1.0", "错误：请输入有效的 BV 号！")
            self.output_textbox.configure(state="disabled")
            return

        try:
            self.urls = get_video_urls(self.bvid)  # Store parsed URLs
            output_text = "解析成功！\nBV 号：{}\n视频地址：\n{}\n".format(self.bvid, "\n".join(self.urls))
        except Exception as e:
            output_text = f"解析失败：{str(e)}"

        self.output_textbox.configure(state="normal")
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("1.0", output_text)
        self.output_textbox.configure(state="disabled")

    def copy_to_clipboard(self):
        """Copy URL to clipboard"""
        if not self.urls:
            self.output_textbox.configure(state="normal")
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("1.0", "错误：没有可复制的 URL！")
            self.output_textbox.configure(state="disabled")
            return
        
        # Copy all URLs to clipboard
        urls_to_copy = "\n".join(self.urls)
        pyperclip.copy(urls_to_copy)  # Use pyperclip to copy
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

class SponsorPage:
    def __init__(self, root):
        self.root = root
        self.create_sponsor_page()

    def create_sponsor_page(self):
        """Create sponsor page, load web content"""
        self.clear_page()
        
        # Create an HtmlFrame to load the webpage
        self.web_frame = tkinterweb.HtmlFrame(self.root, width=960, height=500)
        self.web_frame.load_url("http://dq.foreve.asia")  # Load webpage
        self.web_frame.pack(fill="both", expand=True)

    def clear_page(self):
        """Clear page content (keep menu bar)"""
        for widget in self.root.winfo_children():
            if not isinstance(widget, ctk.CTkFrame):  # Keep the menu bar
                widget.destroy()

class AboutPage:
    def __init__(self, root):
        self.root = root
        self.current_version = "v1.0.0"  # Current version
        self.create_about_page()

    def create_about_page(self):
        """Create about page"""
        self.clear_page()

        # Create main frame for the about interface
        self.about_frame = ctk.CTkFrame(self.root)
        self.about_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        about_label = ctk.CTkLabel(
            self.about_frame,
            text="关于本应用程序",
            font=("SimHei", 16, "bold")
        )
        about_label.pack(pady=10)

        # Current version
        version_label = ctk.CTkLabel(
            self.about_frame,
            text=f"当前程序版本: {self.current_version}",
            font=("SimHei", 14)
        )
        version_label.pack(pady=5, fill="x")

        # Developer info (clickable)
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

        # Repository link (clickable)
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

        # Check for updates (clickable)
        check_update_button = ctk.CTkButton(
            self.about_frame,
            text="检查更新",
            font=("SimHei", 14),
            command=self.check_for_updates
        )
        check_update_button.pack(pady=5, fill="x")

    def check_for_updates(self):
        """Check for updates"""
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
        """Display update information"""
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
        """Display a message"""
        message_label = ctk.CTkLabel(
            self.about_frame,
            text=message,
            font=("SimHei", 14)
        )
        message_label.pack(pady=5, fill="x")

    def open_developer_github(self):
        webbrowser.open("https://github.com/WavesMan")

    def open_repo_github(self):
        webbrowser.open("https://github.com/WavesMan/bilibili-video-parsing")  # Open specified GitHub page

    def clear_page(self):
        """Clear page content (keep menu bar)"""
        for widget in self.root.winfo_children():
            if not isinstance(widget, ctk.CTkFrame):  # Keep the menu bar
                widget.destroy()

def fetch_bilibili_data(bvid):
    api_url = "https://api.bilibili.com/x/web-interface/view"
    params = {'bvid': bvid}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['data']['cid']
        
    except requests.RequestException as e:
        raise Exception("Error making request:", e)
    except json.JSONDecodeError as e:
        raise Exception("Error decoding JSON:", e)
    except KeyError as e:
        raise Exception("Error: 缺少必要的 JSON 键:", e)

def get_video_urls(bvid):
    cid = fetch_bilibili_data(bvid)
    
    selected_model = "64"  # Default to 720P HD

    api_url = "https://api.bilibili.com/x/player/playurl"
    
    output_key = {
        'bvid': bvid,
        'cid': cid,
        'qn': selected_model,
        'fnval': 1,
        'fnver': 0,
        'fourk': 0,
        'platform': 'html5'     
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.bilibili.com/'
    }
    
    try:
        response = requests.get(api_url, params=output_key, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        urls = [i['url'] for i in data['data']['durl']]
        return urls
        
    except requests.RequestException as e:
        raise Exception("Error making request:", e)

if __name__ == "__main__":
    app = MainApplication()
    app.run()
