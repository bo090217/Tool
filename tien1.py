import requests
import json
import time
import threading
import re
import os
from bs4 import BeautifulSoup
import pyfiglet

# In dòng nhiều màu với hiệu ứng xanh đậm nhạt dần
def print_colorful_line(text):
    colors = ['\033[94m', '\033[96m', '\033[97m']
    reset = '\033[0m'
    result = ''
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        result += color + char
    return result + reset

# In banner Nguyen Hieu với hiệu ứng màu xanh đậm-nhạt
def print_colorful_banner(banner_text):
    lines = banner_text.split("\n")
    for line in lines:
        print(print_colorful_line(line))

# Hộp thông tin nhiều màu, căn giữa nội dung
def print_colorful_box():
    reset = '\033[0m'
    text_lines = [
        "DEVELOPER : Nguyễn Hiếu",
        "ADMIN BY : Nguyễn Hiếu",
        "DISCORD : frv_23th04"
    ]
    
    # Tính chiều dài tối đa của dòng và căn giữa
    max_len = max(len(line) for line in text_lines)
    padding = 30  # Căn giữa, bạn có thể điều chỉnh giá trị này để làm rộng hoặc hẹp bảng
    top_bottom = "═" * (max_len + 4)

    print('\033[96m' + "╔" + top_bottom + "╗" + reset)
    for line in text_lines:
        colorful = print_colorful_line(line)
        # Căn giữa văn bản trong bảng
        padding_left = (max_len + 4 - len(line)) // 2
        padding_right = max_len + 4 - len(line) - padding_left
        print('\033[94m' + "║" + ' ' * padding_left + colorful + ' ' * padding_right + "║" + reset)
    print('\033[96m' + "╚" + top_bottom + "╝" + reset)

# Class Messenger
class Messenger:
    def __init__(self, cookie):
        self.cookie = cookie
        self.user_id = self.get_user_id()
        self.fb_dtsg = None
        self.init_params()

    def get_user_id(self):
        try:
            return re.search(r"c_user=(\d+)", self.cookie).group(1)
        except:
            raise Exception("Cookie không hợp lệ")

    def init_params(self):
        headers = {'Cookie': self.cookie, 'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get('https://m.facebook.com', headers=headers)
            match = re.search(r'name="fb_dtsg" value="(.*?)"', response.text)
            if match:
                self.fb_dtsg = match.group(1)
            else:
                raise Exception("Không tìm thấy fb_dtsg")
        except Exception as e:
            raise Exception(f"Lỗi khởi tạo: {str(e)}")

    def send_message(self, recipient_id, message):
        timestamp = int(time.time() * 1000)
        data = {
            'fb_dtsg': self.fb_dtsg,
            '__user': self.user_id,
            'body': message,
            'action_type': 'ma-type:user-generated-message',
            'timestamp': timestamp,
            'offline_threading_id': str(timestamp),
            'message_id': str(timestamp),
            'thread_fbid': recipient_id,
            'source': 'source:chat:web',
            'client': 'mercury'
        }
        headers = {
            'Cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            r = requests.post('https://www.facebook.com/messaging/send/', data=data, headers=headers)
            return r.status_code == 200
        except:
            return False

def send_messages_to_group(group_id, cookie, txt_file, delay):
    messenger = Messenger(cookie)

    # Gửi quảng cáo
    ads = [
        "DEVELOPER : Nguyễn Hiếu",
        "ADMIN BY : Nguyễn Hiếu",
        "DISCORD : frv_23th04"
    ]
    for ad in ads:
        messenger.send_message(group_id, ad)
        time.sleep(delay)

    with open(txt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        message = line.strip()
        if message:
            success = messenger.send_message(group_id, message)
            print(f"Gửi: {message} => {'Thành công' if success else 'Thất bại'}")
            time.sleep(delay)

# Thay đổi màu chữ cho các trường nhập
def print_red_input(prompt):
    red_color = '\033[91m'
    green_color = '\033[92m'
    reset = '\033[0m'
    return input(f"{red_color}[Nguyễn Hiếu] => {green_color}{prompt}: {reset}")

def print_green_input(prompt):
    green_color = '\033[92m'
    reset = '\033[0m'
    return input(f"{green_color}{prompt}: {reset}")

if __name__ == "__main__":
    os.system('clear')
    banner = pyfiglet.figlet_format("Nguyen Hieu", font="big")
    print_colorful_banner(banner)
    print_colorful_box()

    # Nhập ID nhóm, Cookie, file .txt, delay với màu chữ đỏ và xanh lá cây
    group_id = print_red_input("Nhập ID nhóm")
    cookie = print_red_input("Nhập Cookie Facebook")
    txt_file = print_red_input("Nhập File .txt chứa nội dung")
    delay = float(print_red_input("Delay (giây)"))  # Sửa lại để phần [Nguyễn Hiếu] => Delay (giây) có màu đỏ

    send_messages_to_group(group_id, cookie, txt_file, delay)
