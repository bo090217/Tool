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
    colors = [
        '\033[94m',  # Xanh dương đậm
        '\033[96m',  # Xanh dương nhạt
        '\033[97m'   # Trắng
    ]
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

# Hộp thông tin nhiều màu
def print_colorful_box():
    reset = '\033[0m'
    text_lines = [
        "DEVELOPER : Nguyễn Hiếu",
        "ADMIN BY : Nguyễn Hiếu",
        "DISCORD : frv_23th04"
    ]
    max_len = max(len(line) for line in text_lines) + 4
    top_bottom = "═" * max_len

    print('\033[96m' + "╔" + top_bottom + "╗" + reset)
    for line in text_lines:
        colorful = print_colorful_line(line)
        padding = max_len - len(line)
        print('\033[94m' + "║  " + colorful + ' ' * (padding - 2) + "║" + reset)
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
        headers = {
            'Cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0'
        }
        try:
            for url in ['https://www.facebook.com', 'https://mbasic.facebook.com', 'https://m.facebook.com']:
                response = requests.get(url, headers=headers)
                match = re.search(r'name="fb_dtsg" value="(.*?)"', response.text)
                if match:
                    self.fb_dtsg = match.group(1)
                    return
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
            response = requests.post('https://www.facebook.com/messaging/send/', data=data, headers=headers)
            return response.status_code == 200
        except:
            return False

# Gửi tin nhắn vòng lặp
def send_messages_loop(messengers, recipient_ids, message, delay):
    while True:
        for recipient_id in recipient_ids:
            for messenger in messengers:
                success = messenger.send_message(recipient_id, message)
                status = "THÀNH CÔNG" if success else "THẤT BẠI"
                print(f"[{status}] Gửi tới box: {recipient_id}")
                time.sleep(delay)

def main():
    os.system('clear')  # clear màn hình
    banner = pyfiglet.figlet_format("Nguyen Hieu", font="big")
    print_colorful_banner(banner)
    print_colorful_box()

    recipient_ids = []
    print("Nhập ID box (Enter trống hoặc nhập 'done' để kết thúc):")
    while True:
        rid = input("> ").strip()
        if not rid or rid.lower() == 'done':
            break
        recipient_ids.append(rid)

    cookies = []
    print("Nhập cookie (Enter trống hoặc nhập 'done' để kết thúc):")
    while True:
        c = input("> ").strip()
        if not c or c.lower() == 'done':
            break
        cookies.append(c)

    messengers = []
    for i, cookie in enumerate(cookies, 1):
        try:
            m = Messenger(cookie)
            messengers.append(m)
            print(f"Cookie {i}: OK - User ID: {m.user_id}")
        except Exception as e:
            print(f"Cookie {i}: Lỗi - {e}")

    if not messengers:
        print("Không có cookie hợp lệ.")
        return

    try:
        delay = float(input("Delay giữa mỗi lần gửi (giây): "))
    except:
        delay = 5

    message_file = input("Nhập tên file chứa tin nhắn: ")
    try:
        with open(message_file, 'r', encoding='utf-8') as f:
            message = f.read().strip()
    except:
        print("Không đọc được file.")
        return 

    print("\n=== BẮT ĐẦU GỬI ===")
    send_messages_loop(messengers, recipient_ids, message, delay)

if __name__ == "__main__":
    main()
