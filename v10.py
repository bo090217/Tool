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

def create_main_banner() -> Text:
    banner = Text(justify="center")
    banner.append("""
██╗░░░░░░█████╗░░██████╗░██╗███╗░░██║
██║░░░░░██╔══██╗██╔════╝░██║████╗░██║
██║░░░░░██║░░██║██║░░██╗░██║██╔██╗██║
██║░░░░░██║░░██║██║░░╚██╗██║██║╚████║
███████╗╚█████╔╝╚██████╔╝██║██║░╚███║
╚══════╝░╚════╝░░╚═════╝░╚═╝╚═╝░░╚══╝

████████╗░█████╗░░█████╗░██╗░░░░░
╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░
░░░██║░░░██║░░██║██║░░██║██║░░░░░
░░░██║░░░██║░░██║██║░░██║██║░░░░░
░░░██║░░░╚█████╔╝╚█████╔╝███████╗
░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝
""", style="cyan")
    banner.append("\n🌟 TOOL ZALO TREO NHÂY BY NGUYỄN HIẾU 🌟\n", style="magenta")
    banner.append("👑 Admin: NGUYỄN HIẾU\n", style="magenta")
    banner.append("📱 Thông tin liên hệ:\n", style="yellow")
    banner.append("   • Facebook: https://www.facebook.com/nguyenhieu.developed\n", style="cyan")
    banner.append("   • Telegram: t.me/frv_23th04\n", style="cyan")
    banner.append("   • Discord: https://discord.gg/As44GtEs\n", style="cyan")
    banner.append("\nℹ️ Phiên bản: V8.16\n", style="green")
    banner.append(f"⏰ Thời gian: {time.strftime('%I:%M %p, %d/%m/%Y')}\n", style="green")
    banner.append("🔄 Cập nhật lần cuối: 20/05/2025\n", style="yellow")
    banner.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n", style="cyan")
    banner.append("✅ Dịch vụ hot war chỉ từ 50k, ib ngay nhé!\n", style="green")
    banner.append("🚀 Chúc bạn treo bot vui vẻ!\n", style="green")
    banner.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", style="cyan")
    return banner

def create_instructions_panel() -> Panel:
    instructions = Text(justify="left")
    instructions.append("🔹 HƯỚNG DẪN SỬ DỤNG TOOL 🔹\n", style="bold cyan")
    instructions.append("1️⃣ Nhập key xác thực từ web để đăng nhập.\n", style="white")
    instructions.append("2️⃣ Nhập số lượng tài khoản Zalo muốn chạy.\n", style="white")
    instructions.append("3️⃣ Nhập IMEI, Cookie cho từng tài khoản.\n", style="white")
    instructions.append("4️⃣ Nhập tên file .txt chứa nội dung nhây.\n", style="white")
    instructions.append("5️⃣ Nhập delay giữa các tin nhắn (giây).\n", style="white")
    instructions.append("6️⃣ Chọn nhóm từ danh sách để spam (VD: 1,3).\n", style="white")
    instructions.append("✅ Bot sẽ tự động spam vào các nhóm đã chọn.\n", style="bold green")
    instructions.append("⚠️ Lưu ý: Đảm bảo file .txt và cookie hợp lệ!\n", style="bold yellow")
    return Panel(instructions, title="Hướng Dẫn Sử Dụng", border_style="green", box=DOUBLE, width=50, padding=(0, 1))

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

def spam_messages_with_tag(bot, thread_id, thread_type, message_text, delay, running_flag):
    # Chia văn bản thành các dòng
    message_lines = message_text.splitlines()
    
    while running_flag.value:
        for line in message_lines:
            mention = Mention("-1", length=len(line), offset=0)
            try:
                bot.send(Message(text=line, mention=mention), thread_id, thread_type)
                custom_print(f"[✅ Nguyễn Hiếu ] Đã gửi tin nhắn tới nhóm {thread_id}: {line}", style="bold green")
            except Exception as e:
                custom_print(f"[❌] Lỗi gửi tin nhắn: {e}", style="bold red")
            time.sleep(delay)

class Bot(ZaloAPI):
    def __init__(self, api_key, secret_key, imei, session_cookies, message_text, delay):
        super().__init__(api_key, secret_key, imei, session_cookies)
        self.message_text = message_text
        self.delay = delay
        self.running_flags = {}
        self.processes = {}

    def start_spam(self, thread_id, thread_type):
        if thread_id not in self.running_flags:
            self.running_flags[thread_id] = multiprocessing.Value('b', False)
        if thread_id not in self.processes:
            self.processes[thread_id] = None

        if not self.running_flags[thread_id].value:
            self.send(Message(text="""
"""), thread_id, thread_type, ttl=60000)
            self.running_flags[thread_id].value = True
            self.processes[thread_id] = multiprocessing.Process(target=spam_messages_with_tag, args=(self, thread_id, thread_type, self.message_text, self.delay, self.running_flags[thread_id]))
            self.processes[thread_id].start()

    def onMessage(self, *args, **kwargs):
        # Ghi đè để không in thông tin tin nhắn, chấp nhận mọi tham số
        pass

    def onEvent(self, *args, **kwargs):
        # Ghi đè để không in thông tin sự kiện, chấp nhận mọi tham số
        pass

    def onAdminMessage(self, *args, **kwargs):
        # Ghi đè để ngăn thông báo admin như "DZI X MOⱭe"
        pass

    def fetch_groups(self):
        try:
            response = self._get("https://tt-group-wpa.chat.zalo.me/api/group/getlg/v4", params={"zpw_ver": 641, "zpw_type": 30})
            data = response.json()
            if not isinstance(data, dict):
                custom_print("❌ Định dạng phản hồi từ API không hợp lệ", style="bold red")
                return None
            if data.get("error_code") != 0:
                custom_print(f"❌ Lỗi API: Mã lỗi #{data.get('error_code')} - {data.get('error_message', 'Lỗi không xác định')}", style="bold red")
                return None
            results = data.get("data")
            if not results:
                custom_print("❌ Không nhận được dữ liệu từ API", style="bold red")
                return None
            results = self._decode(results)
            if not isinstance(results, dict):
                custom_print("❌ Dữ liệu giải mã không phải dạng dict", style="bold red")
                return None
            results = results.get("data") if results.get("error_code", 0) == 0 else results
            if results is None:
                custom_print("❌ Dữ liệu giải mã là None", style="bold red")
                return None
            if isinstance(results, str):
                try:
                    results = json.loads(results)
                except Exception as e:
                    custom_print(f"❌ Lỗi parse JSON: {e}", style="bold red")
                    return None
            if not isinstance(results, dict):
                custom_print("❌ Cấu trúc dữ liệu không hợp lệ", style="bold red")
                return None
            if "groups" in results and results["groups"]:
                try:
                    group_obj = Group.fromDict(results, None)
                    if not hasattr(group_obj, 'groups') or not group_obj.groups:
                        custom_print("❌ Đối tượng nhóm thiếu 'groups' hoặc rỗng", style="bold red")
                        return None
                    return group_obj
                except Exception as e:
                    custom_print(f"❌ Lỗi parse nhóm: {e}", style="bold red")
            if "gridVerMap" in results:
                group_list = [{"grid": grid} for grid in results["gridVerMap"].keys()]
                fallback_results = {"groups": group_list}
                try:
                    group_obj = Group.fromDict(fallback_results, None)
                    if not hasattr(group_obj, 'groups') or not group_obj.groups:
                        custom_print("❌ Đối tượng nhóm fallback thiếu 'groups' hoặc rỗng", style="bold red")
                        return None
                    return group_obj
                except Exception as e:
                    custom_print(f"❌ Lỗi tạo nhóm fallback: {e}", style="bold red")
            custom_print("❌ Cấu trúc dữ liệu thiếu 'groups' và 'gridVerMap'", style="bold red")
            return None
        except ZaloAPIException as e:
            custom_print(f"❌ Lỗi ZaloAPI: {e}", style="bold red")
            return None
        except Exception as e:
            custom_print(f"❌ Lỗi bất ngờ: {e}", style="bold red")
            return None

    def fetch_group_info(self, group_id):
        try:
            params = {"zpw_ver": 641, "zpw_type": 30}
            payload = {"params": {"gridVerMap": {str(group_id): 0}}}
            payload["params"]["gridVerMap"] = json.dumps(payload["params"]["gridVerMap"])
            payload["params"] = self._encode(payload["params"])
            response = self._post("https://tt-group-wpa.chat.zalo.me/api/group/getmg-v2", params=params, data=payload)
            data = response.json()
            if not isinstance(data, dict):
                custom_print(f"❌ Định dạng phản hồi API không hợp lệ cho nhóm {group_id}", style="bold red")
                return None
            if data.get("error_code") != 0:
                custom_print(f"❌ Lỗi API nhóm {group_id}: Mã lỗi #{data.get('error_code')} - {data.get('error_message', 'Lỗi không xác định')}", style="bold red")
                return None
            results = data.get("data")
            if not results:
                custom_print(f"❌ Không nhận được dữ liệu API cho nhóm {group_id}", style="bold red")
                return None
            results = self._decode(results)
            if not isinstance(results, dict):
                custom_print("❌ Dữ liệu giải mã không phải dict", style="bold red")
                return None
            results = results.get("data") if results.get("error_code", 0) == 0 else results
            if results is None:
                custom_print(f"❌ Dữ liệu giải mã là None cho nhóm {group_id}", style="bold red")
                return None
            if isinstance(results, str):
                try:
                    results = json.loads(results)
                except Exception as e:
                    custom_print(f"❌ Lỗi parse JSON nhóm {group_id}: {e}", style="bold red")
                    return None
            try:
                group_info = Group.fromDict(results, None)
                if hasattr(group_info, 'groups') and group_info.groups:
                    return group_info
            except Exception as e:
                custom_print(f"❌ Lỗi parse thông tin nhóm {group_id}: {e}", style="bold red")
            if isinstance(results, dict) and "gridInfoMap" in results and str(group_id) in results["gridInfoMap"]:
                group_data = results["gridInfoMap"][str(group_id)]
                group_name = group_data.get("name", "Nhóm không xác định")
                total_members = group_data.get("totalMember", 0)
                display_name = f"Nhóm {group_name}" if total_members >= 2 else group_name
                mock_group = type('MockGroup', (), {
                    'groups': [type('MockGroupItem', (), {
                        'grid': group_id,
                        'name': display_name
                    })()]
                })()
                return mock_group
            custom_print(f"❌ Không có thông tin nhóm hợp lệ cho nhóm {group_id}", style="bold red")
            mock_group = type('MockGroup', (), {
                'groups': [type('MockGroupItem', (), {
                    'grid': group_id,
                    'name': 'Nhóm không xác định'
                })()]
            })()
            return mock_group
        except ZaloAPIException as e:
            custom_print(f"❌ Lỗi ZaloAPI nhóm {group_id}: {e}", style="bold red")
            return None
        except Exception as e:
            custom_print(f"❌ Lỗi bất ngờ nhóm {group_id}: {e}", style="bold red")
        return None

def read_file_content(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read().strip()
    except Exception as e:
        custom_print(f"❌ Lỗi đọc file {filename}: {e}", style="bold red")
        return ""

def parse_group_selection(input_str, max_index):
    try:
        numbers = [int(i.strip()) for i in input_str.split(',')]
        return [n for n in numbers if 1 <= n <= max_index]
    except:
        custom_print("❌ Định dạng nhóm không hợp lệ!", style="bold red")
        return []

def start_multiple_accounts():
    console.clear()
    # In banner trước
    console.print(Panel(create_main_banner(), title="Tool Treo Nhây Nguyễn Hiếu", border_style="cyan", box=DOUBLE, width=60, padding=(0, 1)))
    # In hướng dẫn sử dụng sau
    console.print(create_instructions_panel())
    
    try:
        num_accounts = int(Prompt.ask("💠 Nhập số lượng tài khoản Zalo muốn chạy", default="1"))
    except ValueError:
        custom_print("❌ Nhập sai, phải là số nguyên!", style="bold red")
        return

    processes = []

    for i in range(num_accounts):
        console.print(f"\n🔹 Nhập thông tin cho tài khoản {i+1} 🔹", style="bold cyan")
        try:
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

            bot = Bot('api_key', 'secret_key', imei, session_cookies, message_text, delay)
            groups = bot.fetch_groups()

            if not groups or not hasattr(groups, 'groups') or not groups.groups:
                custom_print("⚠️ Không lấy được nhóm nào!", style="bold red")
                continue

            # Tạo bảng danh sách nhóm
            table = Table(show_header=True, header_style="bold cyan", show_lines=False, box=None)
            table.add_column("STT", width=5, justify="center", style="white")
            table.add_column("Tên nhóm", width=25, justify="left", style="bold green")
            table.add_column("ID nhóm", width=15, justify="left", style="cyan")
            
            for idx, group in enumerate(groups.groups, 1):
                info = bot.fetch_group_info(group.grid)
                name = info.groups[0].name if info and hasattr(info, 'groups') else "Nhóm không xác định"
                table.add_row(str(idx), name, str(group.grid))
            
            console.print(Panel(table, title="[bold cyan]📋 Danh sách nhóm[/bold cyan]", border_style="bold cyan", width=50, padding=(0, 1)))

            raw = Prompt.ask("🔸 Nhập số nhóm muốn spam (VD: 1,3)", default="")
            selected = parse_group_selection(raw, len(groups.groups))
            if not selected:
                custom_print("⚠️ Không chọn nhóm nào!", style="bold red")
                continue

            selected_ids = [groups.groups[i - 1].grid for i in selected]

            p = multiprocessing.Process(
                target=start_bot,
                args=('api_key', 'secret_key', imei, session_cookies, message_text, delay, selected_ids)
            )
            processes.append(p)
            p.start()

        except ValueError:
            custom_print("❌ Delay phải là số nguyên!", style="bold red")
            continue
        except Exception as e:
            custom_print(f"❌ Lỗi nhập liệu: {e}", style="bold red")
            continue

    custom_print("\n✅ TẤT CẢ BOT ĐÃ KHỞI ĐỘNG THÀNH CÔNG", style="bold green")

def start_bot(api_key, secret_key, imei, session_cookies, message_text, delay, group_ids):
    bot = Bot(api_key, secret_key, imei, session_cookies, message_text, delay)
    for group_id in group_ids:
        custom_print(f"▶️ Bắt đầu treo nhây nhóm {group_id}", style="bold cyan")
        bot.start_spam(group_id, ThreadType.GROUP)
    bot.listen(run_forever=True, thread=False, delay=1, type='requests')

if __name__ == "__main__":
    while not login_screen():
        pass
    start_multiple_accounts()