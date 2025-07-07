import threading
import time
import re
import requests
import os
import random
import json
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.box import DOUBLE

UA_KIWI = [
    "Mozilla/5.0 (Linux; Android 11; RMX2185) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Redmi Note 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.129 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.68 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; V2031) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.60 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; CPH2481) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Mobile Safari/537.36"
]

UA_VIA = [
    "Mozilla/5.0 (Linux; Android 10; Redmi Note 8) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.0.0 Mobile Safari/537.36 Via/4.8.2",
    "Mozilla/5.0 (Linux; Android 11; V2109) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/112.0.5615.138 Mobile Safari/537.36 Via/4.9.0",
    "Mozilla/5.0 (Linux; Android 13; TECNO POVA 5) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/114.0.5735.134 Mobile Safari/537.36 Via/5.0.1",
    "Mozilla/5.0 (Linux; Android 12; Infinix X6710) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.138 Mobile Safari/537.36 Via/5.2.0",
    "Mozilla/5.0 (Linux; Android 14; SM-A546E) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.112 Mobile Safari/537.36 Via/5.3.1"
]

USER_AGENTS = UA_KIWI + UA_VIA

class NgquanghuyMessenger:
    def __init__(self, cookie):
        self.cookie = cookie
        self.user_id = self.ngquanghuy_id_user()
        self.user_agent = random.choice(USER_AGENTS)
        self.fb_dtsg = None
        self.ngquanghuy_init_params()

    def ngquanghuy_id_user(self):
        try:
            c_user = re.search(r"c_user=(\d+)", self.cookie).group(1)
            return c_user
        except:
            raise Exception("Cookie không hợp lệ")

    def ngquanghuy_init_params(self):
        headers = {
            'Cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }

        try:
            response = requests.get('https://www.facebook.com', headers=headers)
            fb_dtsg_match = re.search(r'"token":"(.*?)"', response.text)

            if not fb_dtsg_match:
                response = requests.get('https://mbasic.facebook.com', headers=headers)
                fb_dtsg_match = re.search(r'name="fb_dtsg" value="(.*?)"', response.text)

                if not fb_dtsg_match:
                    response = requests.get('https://m.facebook.com', headers=headers)
                    fb_dtsg_match = re.search(r'name="fb_dtsg" value="(.*?)"', response.text)

            if fb_dtsg_match:
                self.fb_dtsg = fb_dtsg_match.group(1)
            else:
                raise Exception("Không thể lấy được fb_dtsg")

        except Exception as e:
            raise Exception(f"Lỗi khi khởi tạo tham số: {str(e)}")

    def gui_tn(self, recipient_id, message, max_retries=10):
        for attempt in range(max_retries):
            timestamp = int(time.time() * 1000)
            offline_threading_id = str(timestamp)
            message_id = str(timestamp)

            data = {
                'thread_fbid': recipient_id,
                'action_type': 'ma-type:user-generated-message',
                'body': message,
                'client': 'mercury',
                'author': f'fbid:{self.user_id}',
                'timestamp': timestamp,
                'source': 'source:chat:web',
                'offline_threading_id': offline_threading_id,
                'message_id': message_id,
                'ephemeral_ttl_mode': '',
                '__user': self.user_id,
                '__a': '1',
                '__req': '1b',
                '__rev': '1015919737',
                'fb_dtsg': self.fb_dtsg
            }

            headers = {
                'Cookie': self.cookie,
                'User-Agent': self.user_agent,
                'Accept': '*/*',
                'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://www.facebook.com',
                'Referer': f'https://www.facebook.com/messages/t/{recipient_id}',
                'Host': 'www.facebook.com',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty'
            }

            try:
                response = requests.post(
                    'https://www.facebook.com/messaging/send/',
                    data=data,
                    headers=headers
                )
                if response.status_code != 200:
                    return {
                        'success': False,
                        'error': 'HTTP_ERROR',
                        'error_description': f'Status code: {response.status_code}'
                    }

                if 'for (;;);' in response.text:
                    clean_text = response.text.replace('for (;;);', '')
                    try:
                        result = json.loads(clean_text)
                        if 'error' in result:
                            return {
                                'success': False,
                                'error': result.get('error'),
                                'error_description': result.get('errorDescription', 'Unknown error')
                            }
                        return {
                            'success': True,
                            'message_id': message_id,
                            'timestamp': timestamp
                        }
                    except json.JSONDecodeError:
                        pass

                return {
                    'success': True,
                    'message_id': message_id,
                    'timestamp': timestamp
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': 'REQUEST_ERROR',
                    'error_description': str(e)
                }

def ngquanghuy_read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        custom_print(f"Không tìm thấy file: {file_path}", style="bold red")
        return ""
    except Exception as e:
        custom_print(f"Lỗi khi đọc file: {str(e)}", style="bold red")
        return ""

def ngquanghuy_start_spam(idbox, cookie, delay, message_text):
    try:
        messenger = NgquanghuyMessenger(cookie)
    except Exception as e:
        custom_print(f"Lỗi cookie: {str(e)}", style="bold red")
        return

    mo_dau = "Bot By: Nguyễn Quang Huy\nLink facebook: https://www.facebook.com/voidloveosutsuki\nZalo: 0868371089\nLink zalo bot: https://zalo.me/g/fkrvry389\nLàm hot war chỉ từ 50k ib anh nhé\nChúc các bạn nhây tag vui vẻ"
    messenger.gui_tn(idbox, mo_dau)

    def loop_send():
        if not message_text:
            custom_print("Nội dung tin nhắn trống", style="bold red")
            return
        while True:
            success = messenger.gui_tn(idbox, message_text)
            custom_print(f"Gửi Tin Nhắn {'Thành Công' if success['success'] else 'Thất Bại'}: {message_text[:30]}...", style="bold green" if success['success'] else "bold red")
            time.sleep(delay)

    thread = threading.Thread(target=loop_send)
    thread.daemon = True
    thread.start()

def ngquanghuy_start_multiple_accounts():
    os.system("clear")
    console.print("""
    ╔═╗─╔╗───╔═══╗────────────╔╗─╔╗
    ║║╚╗║║───║╔═╗║────────────║║─║║
    ║╔╗╚╝╠══╗║║─║╠╗╔╦══╦═╗╔══╗║╚═╝╠╗╔╦╗─╔╗
    ║║╚╗║║╔╗║║║─║║║║║╔╗║╔╗╣╔╗║║╔═╗║║║║║─║║
    ║║─║║║╚╝║║╚═╝║╚╝║╔╗║║║║╚╝║║║─║║╚╝║╚═╝║
    ╚╝─╚═╩═╗║╚══╗╠══╩╝╚╩╝╚╩═╗║╚╝─╚╩══╩═╗╔╝
    ─────╔═╝║───╚╝────────╔═╝║───────╔═╝║
    ─────╚══╝─────────────╚══╝───────╚══╝
    🔹 HƯỚNG DẪN SỬ DỤNG TOOL ĐA COOKIE + ĐA BOX 🔹""")
    console.print("1️⃣ Nhập số lượng tài khoản Facebook muốn chạy.")
    console.print("2️⃣ Nhập thông tin Cookie và ID Box cho từng tài khoản.")
    console.print("3️⃣ Nhập tên file chứa nội dung tin nhắn spam.")
    console.print("4️⃣ Nhập thời gian delay giữa các tin nhắn (giây).")
    console.print("✅ Sau khi nhập xong, bot sẽ tự động chạy\n")

    try:
        num_accounts = int(Prompt.ask("💠 Nhập số lượng tài khoản Facebook muốn chạy"))
        if num_accounts < 1:
            custom_print("Số lượng tài khoản phải lớn hơn 0. Thoát chương trình.", style="bold red")
            return
    except ValueError:
        custom_print("Số lượng tài khoản phải là số nguyên. Thoát chương trình.", style="bold red")
        return

    threads = []

    for i in range(num_accounts):
        console.print(f"\n🔹 Nhập thông tin cho tài khoản {i+1} 🔹")
        
        cookie = Prompt.ask("🍪 Nhập Cookie").strip()
        if not cookie:
            custom_print("Cookie không được để trống. Bỏ qua tài khoản này.", style="bold red")
            continue

        idbox_input = Prompt.ask("🆔 Nhập ID box (cách nhau bằng dấu phẩy)").strip()
        idbox_list = [id.strip() for id in idbox_input.split(',') if id.strip()]
        if not idbox_list:
            custom_print("Danh sách ID box trống. Bỏ qua tài khoản này.", style="bold red")
            continue

        file_txt = Prompt.ask("📂 Nhập tên file .txt chứa nội dung spam").strip()
        message_text = ngquanghuy_read_file_content(file_txt)
        if not message_text:
            custom_print("⚠️ File rỗng hoặc lỗi đọc file! Bỏ qua tài khoản này.", style="bold red")
            continue

        try:
            delay = int(Prompt.ask("⏳ Nhập delay giữa các lần gửi (giây)"))
            if delay < 1:
                custom_print("Delay phải là số nguyên dương. Bỏ qua tài khoản này.", style="bold red")
                continue
        except ValueError:
            custom_print("Delay phải là số nguyên. Bỏ qua tài khoản này.", style="bold red")
            continue

        for idbox in idbox_list:
            custom_print(f"Khởi động Treo Ngôn cho ID Box: {idbox} với cookie: {cookie[:30]}...", style="bold yellow")
            thread = threading.Thread(target=ngquanghuy_start_spam, args=(idbox, cookie, delay, message_text))
            threads.append(thread)
            thread.start()

    if not threads:
        custom_print("Không có tài khoản nào được khởi động. Thoát chương trình.", style="bold red")
        return

    custom_print("\nTool đang chạy. Nhấn Ctrl+C để dừng.", style="bold yellow")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        custom_print("\nĐã dừng tool.", style="bold red")
        os._exit(0)

if __name__ == "__main__":
        ngquanghuy_start_multiple_accounts()
