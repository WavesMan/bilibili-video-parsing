# bilibili-video-parsing


---

**bilibili-video-parsing** 是一个基于 `Tkinter` 的图形用户界面应用程序，用于从 Bilibili 获取视频信息并解析视频地址。该项目提供了一个直观的界面，使用户能够轻松输入 BV 号并获取视频链接。
<br>**本项目不同于其他在线解析站，本项目解析结果不依托于任何第三方平台，而是依托 “bilibili-API-collect” 提供的 API 信息直接从 Bilibili 的 API 获取视频信息并解析视频地址。**

[bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)
---

## 项目功能

- **视频信息解析**：通过 Bilibili 的 API 获取视频信息和解析视频地址。
- **用户友好的 GUI**：使用 `Tkinter` 提供图形化界面，用户可以通过简单的输入框与程序交互。
- **复制链接功能**：一键复制解析出的 URL 到剪贴板，方便用户使用。
- **主题切换**：支持 Light/Dark 主题切换，提升用户体验（如适用）。

---

## 项目结构

```
bilibili-video-parsing          
├─ about_page.py                
├─ get_bilibili_stream.py                        
├─ main.py                      
├─ sponsor_page.py              
├─ windowsmanager.py            
├─ README.md                  # 项目说明文档
└─ LICENSE                    # 许可证文件
```

---

## 安装与运行

### 安装前准备

确保您已安装 Python 3.11 或更高版本。

### #Windows/Linux/Mac

1. 克隆项目

```bash
git clone https://github.com/WavesMan/bilibili-video-parsing.git
cd bilibili-video-parsing
```

2. 安装依赖

```bash
pip install -r requirements.txt  # 安装依赖
```

3. 启动程序

```bash
python main.py
# 或（不推荐）
pthon ./asset/gui.py
```

4. 访问 GUI

在弹出的窗口中，输入 Bilibili 的 BV 号，即可获取视频地址。

---

## 依赖说明

- **Python 3.11+**：项目基于 Python 3.11 开发，确保兼容性和性能。
- **Tkinter**：用于创建图形用户界面。
- **Requests**：用于与 Bilibili API 进行 HTTP 请求。
- **Pyperclip**：用于实现剪贴板操作。

---

## 注意事项

1. **网络连接**：确保您的网络连接正常，以便访问 Bilibili API。
2. **BV 号格式**：请确保输入的 BV 号格式正确，以避免解析失败。

---

## 更新日志

### v1.1.0 (初始版本)
- **功能**：
  - 支持输入 BV 号并获取视频信息。
  - 提供图形用户界面，提升用户体验。
  - 实现复制链接功能，将视频地址复制到剪贴板。
- **已知问题**：
  - 暂无已知问题。

---

## 贡献与反馈

欢迎提交 Issue 或 Pull Request 来改进项目！如果有任何问题或建议，请通过以下方式联系：

- **GitHub Issues**: [提交 Issue](https://github.com/WavesMan/bilibili-video-parsing/issues)

---

## 许可证

本项目遵循 [GPL-2.0 License](LICENSE)。

---

## 致谢

- **bilibili-API-collect**：提供 API 支持。
- **Tkinter**：提供 GUI 框架。
- **Requests**：用于简化 HTTP 请求。

---

希望这个 `README.md` 能帮助你更好地展示项目！如果有其他需求，欢迎随时补充或修改！