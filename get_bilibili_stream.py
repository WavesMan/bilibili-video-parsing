import json
import sys
import os
import glob
import platform
import requests
import pyperclip

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
        print("Error making request:", e)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        sys.exit(1)
    except KeyError as e:
        print("Error: 缺少必要的 JSON 键:", e)
        sys.exit(1)

def get_video_urls(bvid):
    cid = fetch_bilibili_data(bvid)
    
    modele_qn = {
        "1": {"text": "360P 流畅", "value": "16"},
        "2": {"text": "480P 标清", "value": "32"},
        "3": {"text": "720P 高清", "value": "64"},
    }

    selected_model = "64"  # 默认选择 720P 高清

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
        print("Error making request:", e)
        sys.exit(1)

if __name__ == "__main__":
    bvid = input("请输入BV号:")
    urls = get_video_urls(bvid)
    for url in urls:
        print(url)
