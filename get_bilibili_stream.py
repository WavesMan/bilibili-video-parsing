import json
import sys
import os
import glob
import platform
import requests
import pyperclip


def fetch_bilibili_data(bvid):
    """从 Bilibili API 获取数据并保存为 JSON 文件"""
    api_url = "https://api.bilibili.com/x/web-interface/view"
    params = {'bvid': bvid}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        output_file = f'{bvid}.json'
        with open(output_file, 'w') as file:
            json.dump(data, file, indent=4)
        
        print(f"成功获取并保存 {bvid}.json 文件")
        return data['data']['cid']
        
    except requests.RequestException as e:
        print("Error making request:", e)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        sys.exit(1)
    except KeyError as e:
        print("Error: 缺少必要的 JSON 键:", e)
        sys.exit(1)

def main():
    while True:
        bvid = input("请输入BV号:")
        cid = fetch_bilibili_data(bvid)

        # 清晰度函数
        modele_qn = {
            "1": {"text": "360P 流畅", "value": "16"},
            "2": {"text": "480P 标清", "value": "32"},
            "3": {"text": "720P 高清", "value": "64"},
            # "下面选项需要登录": {"text":"", "value": "0"},
            # "4": {"text": "720P60 高帧率", "value": "74"}
        }

        # 清晰度函数选择菜单
        def show_model_menu() -> None:
            """显示清晰度选择菜单"""
            print("\n可选清晰度列表：")
            for num, details in modele_qn.items():
                print(f"  [{num}][{details['text']}]")
            print("  [q] 退出")

        # 选择清晰度
        def get_usr_choice() -> str:
            """获取用户选择"""
            while True:
                choice = input("\n请选择清晰度:").strip().lower()
                if choice == 'q':
                    sys.exit("用户取消选择，正在退出")
                if choice in modele_qn:
                    return modele_qn[choice]['value']
                print("Error: 无效的选项，请重新输入")

        show_model_menu()
        selected_model = get_usr_choice()

        #####################################################

        # API URL和参数
        api_url = "https://api.bilibili.com/x/player/playurl"

        # 构建key
        def build_key(bvid, cid, selected_model):
            """构建key字典"""
            return {
                'bvid': bvid,
                'cid': cid,
                'qn': selected_model,  # 请求1080P 高清
                'fnval': 1,  # MP4 格式
                'fnver': 0,  # 视频流版本标识
                'fourk': 0,  # 不请求4K
                'platform': 'html5'     
            }

        # 构建请求的函数
        def make_request(api_url, params):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                'Referer': 'https://www.bilibili.com/'
            }
            try:
                response = requests.get(api_url, params=params, headers=headers)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print("Error making request:", e)
                sys.exit(1)

        output_key = build_key(bvid, cid, selected_model)
        data = make_request(api_url, output_key)

        #####################################################

        # # 打印json数据
        # print("\n\n# json 输出")
        # print(json.dumps(data, indent=4, ensure_ascii=False))

        # 将json数据保存为文件
        with open(f"{bvid}_url.json", 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        #####################################################

        # 读取"{bvid}_url.json"中的url
        with open(f"{bvid}_url.json", 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        #####################################################

        # 删除.json文件
        def delete_json_files():
            # 获取操作系统类型
            system_type = platform.system()
            print(f"检测到的操作系统类型: {system_type}")

            # 定义要删除的文件模式
            pattern = '*.json'
            
            # 查找并删除.json文件
            for file_path in glob.glob(pattern, recursive=True):
                try:
                    os.remove(file_path)
                    print(f"已删除文件: {file_path}")
                except Exception as e:
                    print(f"删除文件 {file_path} 时出错: {e}")
        
        delete_json_files()

        #####################################################

        # 打印url
        print("\n\n# 视频地址")
        for i in data['data']['durl']:
            url = i['url']
            print(url)
            pyperclip.copy(url)
            print(f"\nURL已复制到剪贴板")
            print("\n\n")

        #####################################################
        #                   开发者调试
        #####################################################
        # # 集中一阶段consle输出
        # print("\n\n# consle 输出")
        # print("BV号=",bvid)
        # print("cid=",cid)
        # print(f"清晰度={selected_model}")
        # # 集中二阶段consle输出
        # print("api_url=",api_url)
        # print("构建的key=", output_key)
        # print(f"curl命令=\n{command}")

if __name__ == "__main__":
    main()
