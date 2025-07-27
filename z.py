import multiprocessing
import time
import sys
import json
import requests
from rich.text import Text
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.box import DOUBLE
from rich.table import Table
from zlapi import *
from zlapi.models import *
from threading import Event, Thread
import random

WEB_KEY_URL = "https://raw.githubusercontent.com/bo090217/Tool/main/key1.json"

console = Console()

def custom_print(text, style="white"):
    console.print(text, style=style)

def get_web_key():
    try:
        response = requests.get(WEB_KEY_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        key = data.get("key")
        custom_print(f"[✅] Lấy key từ web thành công!", style="bold green")
        return key
    except (requests.RequestException, json.JSONDecodeError) as e:
        custom_print(f"[❌] Lỗi lấy key từ web: {e}", style="bold red")
        return None

def create_login_banner() -> Text:
    banner = Text(justify="center")
    banner.append("""
╔═╗─╔╗───╔═══╗────────────╔╗─╔╗
║║╚╗║║───║╔═╗║────────────║║─║║
║╔╗╚╝╠══╗║║─║╠╗╔╦══╦═╗╔══╗║╚═╝╠╗╔╦╗─╔╗
║║╚╗║║╔╗║║║─║║║║║╔╗║╔╗╣╔╗║║╔═╗║║║║║─║║
║║─║║║╚╝║║╚═╝║╚╝║╔╗║║║║╚╝║║║─║║╚╝║╚═╝║
╚╝─╚═╩═╗║╚══╗╠══╩╝╚╩╝╚╩═╗║╚╝─╚╩══╩═╗╔╝
─────╔═╝║───╚╝────────╔═╝║───────╔═╝║
─────╚══╝─────────────╚══╝───────╚══╝
""", style="cyan")
    banner.append("\n🌟 TOOL ZALO TREO NHÂY BY NGUYỄN HIẾU 🌟\n", style="magenta")
    banner.append("🔐 Vui lòng nhập key để đăng nhập\n", style="yellow")
    banner.append("ℹ️ Phiên bản: V8.16\n", style="green")
    banner.append(f"⏰ Thời gian: {time.strftime('%I:%M %p, %d/%m/%Y')}\n", style="green")
    return banner

def login_screen() -> bool:
    console.clear()
    console.print(Panel(create_login_banner(), title="Đăng Nhập Tool Zalo Nguyễn Hiếu", border_style="cyan", box=DOUBLE, width=60, padding=(0, 1)))
    key = Prompt.ask("\n🔑 Nhập key xác thực", default="", show_default=False)
    web_key = get_web_key()
    if not web_key:
        custom_print("[❌] Không lấy được key từ web. Kiểm tra URL!", style="bold red")
        time.sleep(2)
        return False
    if key == web_key:
        custom_print("[✅] Đăng nhập thành công!", style="bold green")
        time.sleep(1)
        console.clear() 
        return True
    else:
        custom_print("[❌] Key không hợp lệ! Thử lại.", style="bold red")
        time.sleep(2)
        return False

def create_main_menu():
    menu = Text(justify="center")
    menu.append("""
===============================
|       MENU CHÍNH TOOL       |
===============================
| 1. Chạy BOT ZALO            |
| 2. Tạo Tài Khoản Mới        |
| 3. Thoát                    |
===============================
""", style="cyan")
    return menu

def main_menu():
    console.clear()
    console.print(Panel(create_main_menu(), title="Menu Chính", border_style="cyan", box=DOUBLE, width=60, padding=(0, 1)))
    choice = Prompt.ask("🔹 Vui lòng chọn một hành động (1-3)", default="1")
    
    if choice == "1":
        start_multiple_accounts()
    elif choice == "2":
        create_new_account()  # You will need to implement this function if you want to add the create new account feature.
    elif choice == "3":
        custom_print("🚀 Thoát chương trình!", style="bold green")
        sys.exit()
    else:
        custom_print("❌ Lựa chọn không hợp lệ! Vui lòng chọn lại.", style="bold red")
        time.sleep(2)
        main_menu()

def fetch_groups(imei, session_cookies):
    bot = ZaloAPI('api_key', 'secret_key', imei, session_cookies)
    try:
        groups = bot.fetch_groups()
        if not groups:
            custom_print("⚠️ Không lấy được nhóm nào!", style="bold red")
            return []
        return groups
    except Exception as e:
        custom_print(f"[❌] Lỗi khi lấy nhóm: {e}", style="bold red")
        return []

def fetch_members(imei, session_cookies, group_id):
    bot = ZaloAPI('api_key', 'secret_key', imei, session_cookies)
    try:
        members = bot.fetch_members(group_id)
        if not members:
            custom_print(f"⚠️ Không lấy được thành viên nhóm {group_id}", style="bold red")
            return []
        return members
    except Exception as e:
        custom_print(f"[❌] Lỗi khi lấy thành viên nhóm {group_id}: {e}", style="bold red")
        return []

def tag_user_from_nhay(client, target_uid, thread_id, target_name, delay, imei, session_cookies, stop_event, message_lines):
    typing_api = ZaloAPI('api_key', 'secret_key', imei, session_cookies)
    try:
        for content in message_lines:
            if stop_event.is_set():
                custom_print("⏹️ Dừng spam bởi stop_event.")
                return

            typing_time = random.uniform(2, 5)
            print(f"[Fake Soạn] {content} ({typing_time:.1f}s)")

            try:
                typing_api.set_typing_real(thread_id, ThreadType.GROUP)
            except:
                pass

            time.sleep(typing_time)

            mention_text = f" @{target_name}"
            full_text = content + mention_text
            mention = Mention(target_uid, offset=len(content) + 1, length=len(mention_text.strip()))

            try:
                client.send(Message(text=full_text, mention=mention), thread_id, ThreadType.GROUP)
                custom_print(f"[✓] Gửi thành công tới nhóm {thread_id}, tag: {target_name}", style="bold green")
            except Exception as e:
                custom_print(f"[!] Lỗi gửi: {e}", style="bold red")

            time.sleep(max(delay - typing_time, 0.5))
    except Exception as e:
        custom_print(f"[❌] Lỗi trong vòng lặp spam: {e}", style="bold red")

def start_spam_for_group(imei, session_cookies, group_id, message_lines, delay):
    stop_event = Event()
    bot = ZaloAPI('api_key', 'secret_key', imei, session_cookies)
    members = fetch_members(imei, session_cookies, group_id)

    if members:
        for i, member in enumerate(members, 1):
            print(f"{i}. {member['name']} | {member['id']}")
        try:
            stt_mem = int(input("🎯 Nhập STT người bạn muốn tag: ")) - 1
            user = members[stt_mem]
            print(f"👉 Đang gửi cho: {user['name']} ({user['id']})")
            tag_user_from_nhay(bot, user['id'], group_id, user['name'], delay, imei, session_cookies, stop_event, message_lines)
        except ValueError:
            custom_print(f"[❌] Lỗi chọn người dùng!", style="bold red")

def start_multiple_accounts():
    console.clear()
    console.print(Panel(create_main_banner(), title="Tool Treo Nhây Nguyễn Hiếu", border_style="cyan", box=DOUBLE, width=60, padding=(0, 1)))
    console.print(create_instructions_panel())

    try:
        num_accounts = int(Prompt.ask("💠 Nhập số lượng tài khoản Zalo muốn chạy", default="1"))
    except ValueError:
        custom_print("❌ Nhập sai, phải là số nguyên!", style="bold red")
        return

    processes = []

    for i in range(num_accounts):
        console.print(f"\n🔹 Nhập thông tin cho tài khoản {i+1} 🔹", style="bold cyan")
        imei = Prompt.ask("📱 Nhập IMEI của Zalo")
        cookie_str = Prompt.ask("🍪 Nhập Cookie")
        try:
            session_cookies = eval(cookie_str)
            if not isinstance(session_cookies, dict):
                custom_print("❌ Cookie phải là dictionary!", style="bold red")
                continue
        except:
            custom_print("❌ Cookie không hợp lệ, dùng dạng {'key': 'value'}!", style="bold red")
            continue

        file_txt = Prompt.ask("📂 Nhập tên file .txt chứa nội dung spam")
        message_text = read_file_content(file_txt)
        if not message_text:
            custom_print("⚠️ File rỗng hoặc không đọc được!", style="bold red")
            continue

        delay = int(Prompt.ask("⏳ Nhập delay giữa các lần gửi (giây)", default="5"))

        groups = fetch_groups(imei, session_cookies)
        if not groups:
            continue

        table = Table(show_header=True, header_style="bold cyan", show_lines=False, box=None)
        table.add_column("STT", width=5, justify="center", style="white")
        table.add_column("Tên nhóm", width=25, justify="left", style="bold green")
        table.add_column("ID nhóm", width=15, justify="left", style="cyan")

        for idx, group in enumerate(groups, 1):
            table.add_row(str(idx), group['name'], str(group['id']))

        console.print(Panel(table, title="[bold cyan]📋 Danh sách nhóm[/bold cyan]", border_style="bold cyan", width=50, padding=(0, 1)))

        raw = Prompt.ask("🔸 Nhập số nhóm muốn spam (VD: 1,3)", default="")
        selected = parse_group_selection(raw, len(groups))
        if not selected:
            custom_print("⚠️ Không chọn nhóm nào!", style="bold red")
            continue

        selected_ids = [groups[i - 1]['id'] for i in selected]

        for group_id in selected_ids:
            start_spam_for_group(imei, session_cookies, group_id, message_text.splitlines(), delay)

    custom_print("\n✅ TẤT CẢ BOT ĐÃ KHỞI ĐỘNG THÀNH CÔNG", style="bold green")

if __name__ == "__main__":
    while not login_screen():
        pass
    main_menu()
